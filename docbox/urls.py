from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    (r'^$', 'docbox.views.view_index'),
    
    (r'^writer/project/(?P<project_id>[a-z0-9\.]{0,300})/page(?P<page>[a-z0-9\/\-\.]{0,300})/$', 'docbox.views.view_writer_page'),
    (r'^writer/project(?P<project_id>[a-z0-9\/\.]{0,300})/$', 'docbox.views.view_writer_project'),
    (r'^mnml/mobs/(?P<project_id>[a-z0-9\.]{0,300})/$', 'docbox.views.list_mobs'),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page':'/'}),
#    (r'^writer(?P<url>[a-z0-9\-\_\/\.]{0,300})/$', 'docbox.views.view_writer'),
    (r'^(?P<url>[a-z0-9\-\_\/\.]{1,300})/$', 'docbox.views.view'),

)

