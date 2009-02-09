import os
from PIL import Image
from cStringIO import StringIO
import codecs

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, Template, RequestContext
from django.contrib.auth.decorators import login_required
from django.views.static import serve

from django.forms import ModelForm
from settings import DOCBOX_DOC_ROOT, DEBUG

from page import Page, url_to_filename

from fileutils import *
from filename import clean_filename
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

FILE_TYPE_MAPPINGS = {
    '.jpg':'img',
    '.gif':'img',
    '.png':'img',
    '.png':'img',
    '.mov':'mov',
    '.avi':'mov',
    '.mp3':'aud',
    '.pdf':'doc',
    '.xls':'doc',
    '.doc':'doc'
}

def _type_from_filename(fname):
    ext = os.path.splitext(fname)[1].lower()
    return FILE_TYPE_MAPPINGS.get(ext.lower(), None)

# in the case of a POST request the flash uploader won't send the user's cookie so no login validation can be performed
# this explains the absence of 'login_required' here...
def upload(request, project_id):
    try:
        editor_id = request.GET['editor_id']
        project = Project.objects.get(identifier=project_id)

        if request.method == 'GET':
            return render_to_response('mnml/upload.html', 
                {'project_id': project_id, 'editor_id': editor_id }, 
                context_instance=RequestContext(request))
        elif request.method == 'POST':
            mob_path = project.file_path
            try:
                os.makedirs(mob_path)
                print "ok"
            except OSError, (errno, strerror):
                print "not ok"
                if errno != 17: # File already exists, in this case, the directory.
                    _log("=ERR=", "makedirs", errno, strerror, mob_path)
                    raise strerror
            mob_file = request.FILES['Filedata']
            fname = mob_file.name
            content_type = _type_from_filename(fname)
            raw_contents = mob_file.read()
            clean_fname = clean_filename(fname)

            if content_type == "mov":
                pass
            #     _upload_movie(link_type, link_id, mob_path, clean_fname, raw_contents)
            elif content_type == "img":
                _upload_image(project_id, mob_path, clean_fname, raw_contents)
            elif content_type == "aud":
                pass
            #     _upload_audio(link_type, link_id, mob_path, clean_fname, raw_contents)
            elif content_type == "doc":
                pass
            #     _upload_document(link_type, link_id, mob_path, clean_fname, raw_contents)
            else:
                ext = os.path.splitext(fname)[1].lower()
                # _log("unknown filetype", ext, clean_fname)
                # todo: make sure this gets mentioned to the user
                return HttpResponse("Unknown filetype %s" % ext, status=400)

#            _log("upload_done", link_type, link_id, clean_fname)
            return render_to_response('mnml/upload_done.html', 
                {'project_id': project_id, 'editor_id': editor_id }, 
                context_instance=RequestContext(request))
    except:
        if DEBUG:
            import sys
            import traceback
            etype, value, tb = sys.exc_info()
            # _log("=ERR= %s" % '\n'.join(traceback.format_exception(etype, value, tb)))
            traceback.print_exception(etype, value, tb)

@login_required
def list_mobs(request, project_id):
    project = Project.objects.get(identifier=project_id)
    editor_id = request.GET['editor_id']

    images = project.get_images()
    audio = project.get_audio()
    movies = project.get_movies()
    documents = project.get_documents()

    return render_to_response('mnml/list_mobs.html', 
        {'project': project, 'images': images, 'audio': audio, 'movies': movies, 'documents': documents, 'editor_id': editor_id }, 
        context_instance=RequestContext(request))

def size_for(width, height, maxwidth=None, maxheight=None):
    """Returns a new width and height pair that fall inside of the given maximum width/height.
    Note that if the given width and height are both smaller than maxwidth and maxheight,
    they are simply returned.
    """
    if maxheight is None or (maxwidth is not None and width > maxwidth and width > height):
        scale = float(maxwidth) / width
        return ( int(width * scale), int(height * scale) )
    elif maxwidth is None or (maxheight is not None and height > maxheight and height >= width):
        scale = float(maxheight) / height
        return ( int(width * scale), int(height * scale) )
    else:
        return width, height        

def universal_resize(img, maxwidth, maxheight):
    """Given a target PIL image, returns a resized version up to the maximum width and height.
    Will only scale images down, not enlarge them.
    - img: original image
    - maxwidth: maximum width of the new image
    - maxheight: maximum height of the new image
    """
    width, height = img.size
    new_width, new_height = size_for(width, height, maxwidth, maxheight)
    resized_img = img.resize( (new_width, new_height), Image.ANTIALIAS )
    return resized_img

def _upload_image(project_id, mob_path, clean_fname, raw_contents):
    dest_fname = os.path.join(mob_path, clean_fname)
    print dest_fname
    thumb_fname = os.path.join(mob_path, "thumb-" + clean_fname)
    print thumb_fname

    sio = StringIO(raw_contents)

    img = Image.open(sio)
    universal_resize(img, 550, 550).save(dest_fname)
    universal_resize(img, 100, 100).save(thumb_fname)
    print img

    return True

