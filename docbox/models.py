import os
from django.db import models
from docbox.util import svn as svnutil

try:
    from settings import DOCBOX_DOC_ROOT
except:
    DOCBOX_DOC_ROOT = ''

FILE_TYPE_MAPPINGS = {
    'img': ['.jpg', '.gif', '.png'],
    'mov': ['.mov', '.avi'],
    'aud': ['.mp3'],
    'doc': ['.pdf', '.xls', '.doc']
}

class Project(models.Model):
    VCS_CHOICES = (
            ('git', 'Git'),
            ('svn', 'Subversion'),
        )
    name = models.CharField(max_length=120)
    identifier = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    homepage = models.URLField(blank=True)
    doc_vcs = models.CharField(max_length=3, choices=VCS_CHOICES, verbose_name='Doc Version Control', blank=True)
    src_vcs = models.CharField(max_length=3, choices=VCS_CHOICES, verbose_name='Source Version Control', blank=True)
    doc_url = models.CharField(max_length=200, verbose_name='Documentation URL', blank=True)
    src_url = models.CharField(max_length=200, verbose_name='Source URL', blank=True)
    
    def _get_file_path(self):
        return os.path.join(DOCBOX_DOC_ROOT, self.identifier)
    file_path = property(_get_file_path)
    
    def _get_absolute_url(self):
        return "/%s/edit/" % self.identifier
    absolute_url = property(_get_absolute_url)
    
    def page_path(self, page):
        return os.path.join(DOCBOX_DOC_ROOT, self.identifier, page + '.html')

    def find_project_files_by_ext(self, extList, with_extension=True):
        li = []
        for f in os.listdir(self.file_path):
            fname, ext = os.path.splitext(f)
            if fname != "" and ext.lower() in extList:
                if with_extension:
                    li.append(f)
                else:
                    li.append(fname)
        return li

    def pages(self):
        return self.find_project_files_by_ext(['.html'], False)
        
    def get_images(self):
        images = self.find_project_files_by_ext(FILE_TYPE_MAPPINGS['img'])
        images = [img for img in images if not img.startswith('thumb-')]
        return images
        
    def get_audio(self):
        return self.find_project_files_by_ext(FILE_TYPE_MAPPINGS['aud'])

    def get_movies(self):
        return self.find_project_files_by_ext(FILE_TYPE_MAPPINGS['mov'])

    def get_documents(self):
        return self.find_project_files_by_ext(FILE_TYPE_MAPPINGS['doc'])
    
    def checkout(self):
        if self.doc_vcs == 'svn':
            svnutil.checkout(self)
        elif self.doc_vcs == 'git': 
            pass # todo: implement
        else:
            try:
                os.mkdir(self.file_path)
            except: # todo: implement
                print "error: '%s' not created." % self.file_path

    def add(self, page_name):
        if self.doc_vcs == 'svn':
            svnutil.addFile(self.page_path(page_name))
        elif self.doc_vcs == 'git': 
            pass # todo: implement
        else:
            pass # todo: implement

    def commit(self, commitString):
        if self.doc_vcs == 'svn':
            svnutil.apply_commit(self.file_path, commitString)
        elif self.doc_vcs == 'git': 
            pass # todo: implement
        else:
            pass # todo: implement

    def revert(self):
        if self.doc_vcs == 'svn':
            svnutil.apply_revert(self.file_path)
        elif self.doc_vcs == 'git': 
            pass # todo: implement
        else:
            pass # todo: implement

    def docChanges(self):
        if self.doc_vcs == 'svn':
            return svnutil.docChanges(self)
        elif self.doc_vcs == 'git': 
            return [] # todo: implement
        else:
            return [] # todo: implement

    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return self.identifier
    
    class Meta:
        ordering = ['identifier']
        