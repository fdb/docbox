import os
import pysvn
import shutil

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
    
def docChanges(project):
    client = pysvn.Client()
    changes = [c.path for c in client.status(project.file_path) if c.text_status != pysvn.wc_status_kind.normal]
    changes = [os.path.splitext(os.path.basename(c))[0] for c in changes]
    return changes
    