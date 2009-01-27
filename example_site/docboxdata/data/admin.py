from django.contrib import admin
from docboxdata.data.models import Project

class ProjectAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Project, ProjectAdmin)
