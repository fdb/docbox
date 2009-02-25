from settings import DOCBOX_URL, DOCBOX_MEDIA_URL

def url(request):
    return {'DOCBOX_URL': DOCBOX_URL, }

def media(request):
    return {'DOCBOX_MEDIA_URL': DOCBOX_MEDIA_URL, }
    