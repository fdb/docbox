
from south.db import db
from django.db import models
from docbox.models import *

class Migration:
    
    def forwards(self):
        VCS_CHOICES = (
                ('git', 'Git'),
                ('svn', 'Subversion'),
            )
        # Model 'Project'
        db.create_table('docbox_project', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('name', models.CharField(max_length=120)),
            ('identifier', models.CharField(max_length=30, unique=True)),
            ('description', models.TextField(blank=True)),
            ('username', models.CharField(max_length=30)),
            ('password', models.CharField(max_length=30)),
            ('homepage', models.URLField(blank=True)),
            ('doc_vcs', models.CharField(max_length=3, choices=VCS_CHOICES, verbose_name='Doc Version Control', blank=True)),
            ('src_vcs', models.CharField(max_length=3, choices=VCS_CHOICES, verbose_name='Source Version Control', blank=True)),
            ('doc_url', models.CharField(max_length=200, verbose_name='Documentation URL', blank=True)),
            ('src_url', models.CharField(max_length=200, verbose_name='Source URL', blank=True)),
        ))
        
        db.send_create_signal('docbox', ['Project'])
    
    def backwards(self):
        db.delete_table('docbox_project')
        
