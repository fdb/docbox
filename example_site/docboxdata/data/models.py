from django.db import models
import os
from settings import DOCBOX_DOC_ROOT

class Project(models.Model):
    name = models.CharField(max_length=120)
    identifier = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    homepage = models.URLField(blank=True)
    doc_url = models.CharField(max_length=200, verbose_name='Documentation URL', blank=True)
    src_url = models.CharField(max_length=200, verbose_name='Source URL', blank=True)
    
    def _get_file_path(self):
        return os.path.join(DOCBOX_DOC_ROOT, self.identifier)
    file_path = property(_get_file_path)
    
    def _get_absolute_url(self):
        return "/writer/project/%s/" % self.identifier
    absolute_url = property(_get_absolute_url)
    
    def page_path(self, page):
        return os.path.join(DOCBOX_DOC_ROOT, self.identifier, page + '.html')

    def pages(self):
        li = []
        for root, dirs, files in os.walk(os.path.join(DOCBOX_DOC_ROOT, self.identifier)):
            for f in files:
                fname, ext = os.path.splitext(f)
                if fname != "" and ext == '.html':
                    li.append(fname)
        return li
    
    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return self.identifier
    
    class Meta:
        ordering = ['identifier']
        