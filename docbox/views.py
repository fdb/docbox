import os

from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, Template, RequestContext

from page import Page, url_to_filename

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