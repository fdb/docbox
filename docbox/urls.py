from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'docbox.views.view_index'),
    (r'^(?P<url>[a-z0-9\/\.]{1,300})/$', 'docbox.views.view'),
)

