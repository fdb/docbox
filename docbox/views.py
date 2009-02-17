import os
import codecs

from settings import DOCBOX_DOC_ROOT, DEBUG

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, Template, RequestContext
from django.contrib.auth.decorators import login_required
from django.views.static import serve
from django.forms import ModelForm

from page import Page, url_to_filename
from docboxdata.data.models import Project
from util.fileio import read_from_file, write_to_file

def format_string(title):
    return title.lower().replace(' ', '_')

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'identifier', 'description', 'homepage', 'vcs', 'src_url', 'doc_url')

def view_index(request):
    return view(request, 'index')

def view(request, url):
    fname = url_to_filename(url)
    print fname
    if os.path.exists(fname):
        page = Page.from_file(fname)
        page_content = page.render(request)

        return render_to_response('docbox/view.html', {'page': page, 'page_content': page_content}, 
            context_instance=RequestContext(request))
    else:
        raise Http404()

def static_serve(request, project_id, filename):
    if project_id.startswith("/"):
        project_id = project_id[1:]
    project = get_object_or_404(Project, identifier=project_id)
    return serve(request, os.path.join(project.identifier, filename), document_root=DOCBOX_DOC_ROOT)

@login_required
def view_writer_project(request, project_id):
    if project_id is not None and project_id != '':
        if project_id.startswith("/"):
            project_id = project_id[1:]
        project = get_object_or_404(Project, identifier=project_id)
        form = ProjectForm(instance = project)
    else:
        project = None
        form = ProjectForm()

    projects = Project.objects.all()

    if request.META["REQUEST_METHOD"] == "POST":
        post = request.POST

        if handle_commit_or_revert(post, project):
            return HttpResponseRedirect(request.META["PATH_INFO"])

        form = ProjectForm(post, instance=project)

        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.identifier = format_string(new_project.identifier)
            new_project.save()
            new_project.checkout()
            return HttpResponseRedirect("/writer/project/" + new_project.identifier + '/')

    changes = project is not None and project.docChanges() or []

    return render_to_response('docbox/view_writer_project.html', 
        {'form': form, 'projects': projects, 'project': project, 'changes': changes }, 
        context_instance=RequestContext(request))

def handle_commit_or_revert(post, project):
    if post.has_key("commit"):
        project.commit(post.get("commitString", ""))
        return True
    elif post.has_key("revert"):
        project.revert()
        return True
    return False

@login_required
def view_writer_page(request, project_id, page):
    is_new = page is None or page == ""
    project = get_object_or_404(Project, identifier=project_id)

    projects = Project.objects.all()

    page_name_error = None
    
    if not is_new:
        if page.startswith("/"):
            title = page = page[1:]
        f = project.page_path(title)
        if not os.path.exists(f):
            raise Http404
        documentation = read_from_file(f)
    else:
        documentation = ''

    if request.META["REQUEST_METHOD"] == "POST":
        post = request.POST

        if handle_commit_or_revert(post, project):
            return HttpResponseRedirect(request.META["PATH_INFO"])

        page_name = is_new and post.get("page-name", "") or page
        documentation = post.get("doc-content", "")
        if page_name == "":
            page_name_error = "Page name can't be empty"
        else:
            filepath = project.page_path(page_name)
            write_to_file(filepath, documentation)
            if is_new:
                project.add(page_name)
            return HttpResponseRedirect("/writer/project/" + project.identifier + '/page/' + page_name + '/')

    changes = project.docChanges()
        
    return render_to_response('docbox/view_writer_page.html', 
        {'project': project, 'documentation': documentation, 'page': page, 'changes': changes, 'projects': projects, 'page_name_error': page_name_error }, 
        context_instance=RequestContext(request))

