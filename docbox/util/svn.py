import os
import pysvn

def apply_commit(project_path, commitString):
    client = pysvn.Client()
    def get_log_message():
        return True, "svn commit"
    client.callback_get_log_message = get_log_message
    client.checkin(project_path, commitString)

def apply_revert(project_path):
    client = pysvn.Client()
    client.revert(project_path, recurse=True)

def checkout(project):
    client = pysvn.Client()
    client.checkout(project.doc_url, project.file_path)

def addFile(path):
    client = pysvn.Client()
    client.add(path)

ALLOWED_EXTENSIONS = [".html", ".gif", ".jpg", ".png", ".avi", ".mov", ".mp3", ".pdf", ".doc", ".xls"]

class StatusObject(object):
    def __init__(self, project, status_object):
        self.project = project
        self.status_object = status_object

    def _get_text_status(self):
        return str(self.status_object.text_status)
    text_status = property(_get_text_status)
        
    def _get_extension(self):
        base, ext = os.path.splitext(os.path.basename(self.status_object.path))
        return ext.lower()
    extension = property(_get_extension)
        
    def _get_basename(self):
        base, ext = os.path.splitext(os.path.basename(self.status_object.path))
        return base
    basename = property(_get_basename)

    def _get_filename(self):
        return os.path.basename(self.status_object.path)
    filename = property(_get_filename)

    def _get_displayname(self):
        return self.isHTML() and self.basename or self.filename
    displayname = property(_get_displayname)
    
    def _get_absolute_url(self):
        return "%s%s/" % (self.project.absolute_url(), self.basename)
    absolute_url = property(_get_absolute_url)
    
    def _get_view_url(self):
        if self.isHTML():
            return "%sedit/" % self.absolute_url
        else:
            return "%s%s" % (self.project.media_url(), self.filename)
    view_url = property(_get_view_url)
    
    def isHTML(self):
        return self.extension == '.html'
        
def docChanges(project):
    client = pysvn.Client()
    changes = [StatusObject(project, c) for c in client.status(project.file_path)]
    changes = [c for c in changes if c.text_status not in ["normal", "unversioned"] and c.extension in ALLOWED_EXTENSIONS]
    return changes
    