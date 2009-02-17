from django.db import models
import os

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
    vcs = models.CharField(max_length=3, choices=VCS_CHOICES, blank=True)
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
    
    def usesGit(self):
        return self.vcs == 'git'
        
    def usesSvn(self):
        return self.vcs == 'svn'

    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return self.identifier
    
    class Meta:
        ordering = ['identifier']
        