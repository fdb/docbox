from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=120)
    identifier = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    homepage = models.URLField(blank=True)
    doc_url = models.CharField(max_length=200, verbose_name='Documentation URL', blank=True)
    src_url = models.CharField(max_length=200, verbose_name='Source URL', blank=True)
    
    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return self.identifier
    
    class Meta:
        ordering = ['identifier']
        