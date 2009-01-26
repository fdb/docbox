from django.contrib import admin
from docboxdata.data.models import Project, VersionURL, SourceURL, DocStatus

class VersionURLAdmin(admin.ModelAdmin):
    pass

class SourceURLAdmin(admin.ModelAdmin):
    pass
    
class ProjectAdmin(admin.ModelAdmin):
    pass

class DocStatusAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(VersionURL, VersionURLAdmin)
admin.site.register(SourceURL, SourceURLAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(DocStatus, DocStatusAdmin)
