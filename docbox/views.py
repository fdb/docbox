import os
import codecs

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, Template, RequestContext
from django.contrib.auth.decorators import login_required
from django.views.static import serve

from django.forms import ModelForm
from settings import DOCBOX_DOC_ROOT

from page import Page, url_to_filename

from fileutils import *
from svnutils import *

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'identifier', 'description', 'homepage', 'src_url', 'doc_url')

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
        form = ProjectForm(post, instance=project)

        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.identifier = format_string(new_project.identifier)
            new_project.save()
            checkout(new_project)
            return HttpResponseRedirect("/writer/project/" + new_project.identifier + '/')

    return render_to_response('docbox/view_writer_project.html', 
        {'form': form, 'projects': projects, 'project': project }, 
        context_instance=RequestContext(request))

def handle_commit(post, project):
    filepath = project.file_path
    if post.has_key("commit"):
        commitString = post.get("commitString", "")
        apply_commit(filepath, commitString)
        return HttpResponseRedirect(project.absolute_url)
    elif post.has_key("revert"):
        apply_revert(filepath)
        return HttpResponseRedirect(project.absolute_url)
    else:
        return None

@login_required
def view_writer_page(request, project_id, page):
    is_new = page is None or page == ""
    project = get_object_or_404(Project, identifier=project_id)

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
        commit = handle_commit(post, project)
        if commit is not None:
            return commit

        title = is_new and post.get("page-name", "") or page
        if title == "":
            raise
        documentation = post.get("doc-content", "")
        filepath = project.page_path(title)
        write_to_file(filepath, documentation)
        if is_new:
            addFile(filepath)
    changes = docChanges(project)
        
    return render_to_response('docbox/view_writer_page.html', 
        {'project': project, 'documentation': documentation, 'page': page, 'changes': changes }, 
        context_instance=RequestContext(request))

@login_required
def list_mobs(request, project_id):
    project = Project.objects.get(identifier=project_id)
    editor_id = request.GET['editor_id']

    images = project.get_images()
    audio = project.get_audio()
    movies = project.get_movies()
    documents = project.get_documents()

    return render_to_response('docbox/view_mobs.html', 
        {'project': project, 'images': images, 'audio': audio, 'movies': movies, 'documents': documents, 'editor_id': editor_id }, 
        context_instance=RequestContext(request))
