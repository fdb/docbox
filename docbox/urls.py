from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'^$', 'docbox.views.view_index'),
    (r'^project/add/$', 'docbox.views.view_writer_project', {'project_id': None}), 
    (r'^(?P<project_id>[a-z0-9\.]{0,300})/edit/$', 'docbox.views.view_writer_project'),

    (r'^(?P<project_id>[a-z0-9\.]{0,300})/page/add/$', 'docbox.views.view_writer_page', {'page': ''}),
    (r'^(?P<project_id>[a-z0-9\.]{0,300})/(?P<page>[a-z0-9\/\-\.]{0,300})/edit/$', 'docbox.views.view_writer_page'),

    (r'^project(?P<project_id>[a-z0-9\/\.]{0,300})/(?P<filename>[a-z0-9\/\-\.]{0,300}(.jpg|.png|.gif|.pdf|.doc|.xls|.mp3|.mov|.avi))$', 'docbox.views.static_serve'),

    (r'^mnml/mobs/(?P<project_id>[a-z0-9\.]{0,300})/$', 'docbox.mnml.views.list_mobs'),
    (r'^mnml/upload/(?P<project_id>[a-z0-9\.]{0,300})/$', 'docbox.mnml.views.upload'),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page':'/'}),
    (r'^(?P<url>[a-z0-9\-\_\/\.]{1,300})/$', 'docbox.views.view'),
)

