import os
import Image

from cStringIO import StringIO

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, Template, RequestContext
from django.contrib.auth.decorators import login_required

from docbox.models import Project
from docbox.util import image as image_util
from docbox.util.filename import clean_filename
from docbox.util import svn
from docbox.mnml import Mob

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
            except OSError, (errno, strerror):
                if errno != 17: # File already exists, in this case, the directory.
                    _log("=ERR=", "makedirs", errno, strerror, mob_path)
                    raise strerror
            mob_file = request.FILES['Filedata']
            fname = mob_file.name
            content_type = _type_from_filename(fname)
            raw_contents = mob_file.read()
            clean_fname = clean_filename(fname)

            if content_type in ["mov", "aud", "doc"]:
                _upload_mob(mob_path, clean_fname, raw_contents)
            elif content_type == "img":
                _upload_image(mob_path, clean_fname, raw_contents)
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
    project = get_object_or_404(Project, identifier=project_id)
    editor_id = request.GET['editor_id']

    images = [Mob(project, image, 'img') for image in project.get_images()]
    audio = [Mob(project, audio_file, 'aud') for audio_file in project.get_audio()]
    movies = [Mob(project, movie_file, 'mov') for movie_file in project.get_movies()]
    documents = [Mob(project, document, 'doc') for document in project.get_documents()]

    return render_to_response('mnml/list_mobs.html', 
        {'project': project, 'images': images, 'audio': audio, 'movies': movies, 'documents': documents, 'editor_id': editor_id }, 
        context_instance=RequestContext(request))

def _upload_image(mob_path, clean_fname, raw_contents):
    dest_fname = os.path.join(mob_path, clean_fname)
    thumb_fname = os.path.join(mob_path, "thumb-" + clean_fname)

    sio = StringIO(raw_contents)

    img = Image.open(sio)
    image_util.universal_resize(img, 550, 550).save(dest_fname)
    image_util.universal_resize(img, 100, 100).save(thumb_fname)

    svn.addFile(dest_fname)
    svn.addFile(thumb_fname)

def _upload_mob(mob_path, clean_fname, raw_contents):
    dest_fname = os.path.join(mob_path, clean_fname)

    file = open(dest_fname, 'wb')
    file.write(raw_contents)
    file.close()

    svn.addFile(dest_fname)
