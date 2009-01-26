from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'', include('docboxdata.urls')),
    (r'', include('docbox.urls')),
)
