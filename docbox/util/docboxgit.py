import os
import git

def apply_commit_and_push(project_path, commitString):
    client = git.Git(project_path)
    client.commit(("-m", commitString))
    client.push()

def apply_revert(project_path):
    client = git.Git(project_path)
    client.checkout("-f")

def clone(project, clone_into):
    client = git.Git(clone_into)
    client.clone(project.doc_url, project.identifier)

def addFile(path):
    client = git.Git(os.path.dirname(path))
    client.add(os.path.basename(path))

ALLOWED_EXTENSIONS = [".html", ".gif", ".jpg", ".png", ".avi", ".mov", ".mp3", ".pdf", ".doc", ".xls"]

# class StatusObject(object):
#     def __init__(self, project, status_object):
#         self.project = project
#         self.status_object = status_object
# 
#     def _get_text_status(self):
#         return str(self.status_object.text_status)
#     text_status = property(_get_text_status)
#         
#     def _get_extension(self):
#         base, ext = os.path.splitext(os.path.basename(self.status_object.path))
#         return ext.lower()
#     extension = property(_get_extension)
#         
#     def _get_basename(self):
#         base, ext = os.path.splitext(os.path.basename(self.status_object.path))
#         return base
#     basename = property(_get_basename)
# 
#     def _get_filename(self):
#         return os.path.basename(self.status_object.path)
#     filename = property(_get_filename)
# 
#     def isHTML(self):
#         return self.extension == '.html'
#         
# def docChanges(project):
#     client = pysvn.Client()
#     changes = [StatusObject(project, c) for c in client.status(project.file_path)]
#     changes = [c for c in changes if c.text_status != "normal" and c.extension in ALLOWED_EXTENSIONS]
#     return changes
