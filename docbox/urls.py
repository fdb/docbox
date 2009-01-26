from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    (r'^$', 'docbox.views.view_index'),
    (r'^writer(?P<url>[a-z0-9\-\_\/\.]{0,300})/$', 'docbox.views.view_writer'),
    (r'^(?P<url>[a-z0-9\-\_\/\.]{1,300})/$', 'docbox.views.view'),

)

