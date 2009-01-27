import os

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, Template, RequestContext
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

        return render_to_response('docbox/view.html', {'page': page, 'page_content':page_content}, 
            context_instance=RequestContext(request))
    else:
        raise Http404()

def handle_commit(post, project):
    if post.has_key("commit"):
        commitString = post.get("commitString", "")
        apply_commit(commitString)
        return HttpResponseRedirect("/writer/" + (project is not None and project.identifier + '/' or ''))

    elif post.has_key("cancelCommit"):
        cancel_commit()
        if project is not None:
            id = project.id
            try:
                Project.objects.get(id=id) # a newly created project won't exist anymore after cancellation so we have to check if it does.
                return HttpResponseRedirect("/writer/" + project.identifier + '/')
            except:
                pass
        return HttpResponseRedirect("/writer/")

    return None
    
def view_writer_with_form(request, url):
    if url is not None and url != '':
        if url.startswith("/"):
            url = url[1:]
        project = get_object_or_404(Project, identifier=url)
    else:
        project = None
    projects = Project.objects.all()
    documentation = ''
#    docstates = DocStatus.objects.all()

    if request.META["REQUEST_METHOD"] == "POST":
        post = request.POST
        commit = handle_commit(post, project)
        if commit is not None:
            return commit

        form = ProjectForm(post, instance=project)
        type = project is not None and 'U' or 'C'
        documentation = post.get("doc-content", "")

        if form.is_valid():
            project = form.save(commit=False)
            project.identifier = format_string(project.identifier)
            project.save()

#            docstatus, created = DocStatus.objects.get_or_create(project=project, defaults={'type': type}) 
#            if created and type == 'C':
#                docstatus.save()

            # if type == 'C' or read_from_file(project.identifier) != documentation:
            #     if created and type == 'U':
            #         copyfile(project)
            #     if write_to_file(documentation, project.identifier):
            #         if created and type == 'U':
            #             docstatus.save()
            return HttpResponseRedirect("/writer/" + project.identifier + '/')
    elif project is not None:
        form = ProjectForm(instance = project)
        documentation = read_from_file(project.identifier)
    else:
        form = ProjectForm()
        
    return render_to_response('docbox/view_writer.html', 
        {'projects': projects, 'project': project, 'form': form, 'documentation': documentation, }, 
        context_instance=RequestContext(request))

if Project is not None:
    view_writer = view_writer_with_form



