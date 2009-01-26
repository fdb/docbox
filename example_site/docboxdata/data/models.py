from django.db import models

class VersionURL(models.Model):
    url = models.CharField(max_length=200, verbose_name='Documentation URL', blank=True)
    working_url = models.CharField(max_length=200, verbose_name='Documentation URL', blank=True)

    def __unicode__(self):
        return self.url

class SourceURL(models.Model):
    url = models.CharField(max_length=200, verbose_name='Source URL', blank=True)

    def __unicode__(self):
        return self.url

class Project(models.Model):
    name = models.CharField(max_length=120)
    identifier = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    homepage = models.URLField(blank=True)
    doc_url = models.CharField(max_length=200, verbose_name='Documentation URL', blank=True)
    src_url = models.CharField(max_length=200, verbose_name='Source URL', blank=True)
    documentation_url = models.ForeignKey(VersionURL, null=True)
    source_url = models.ForeignKey(SourceURL, null=True)
    
    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return self.identifier
    
    class Meta:
        ordering = ['identifier']
        
class DocStatus(models.Model):
    project = models.ForeignKey(Project)
    type = models.CharField(max_length=2, choices=(('C', 'Create'), ('U', 'Update')))
