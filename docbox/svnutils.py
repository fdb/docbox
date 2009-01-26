import os
import pysvn
import shutil
from settings import DOCBOX_DOC_ROOT
from docboxdata.data.models import Project, DocStatus
from fileutils import format_string

def copy_files_to_working_copy():
    client = pysvn.Client()
    for docstatus in DocStatus.objects.all():
        project = docstatus.project
        filename = format_string(project.identifier)
        f = os.path.join(DOCBOX_DOC_ROOT, filename + '.html')
        doc_url = project.documentation_url.working_url
        c = os.path.join(doc_url, filename + '.html')
        path = os.path.dirname(c)
        # create directories in working copy and put them in version control
        if not os.path.exists(path):
            p = ''
            for l in filename.split('/')[:-1]:
                p += '/%s' % l
                if not os.path.exists(os.path.join(doc_url, p[1:])):
                    client.mkdir(os.path.join(doc_url, p[1:]), '...')
        shutil.copy(f, c)
        if docstatus.type == 'C':
            client.add(c)

def delete_backup_files():
    for docstatus in DocStatus.objects.filter(type='U'):
        try:
            filename = format_string(docstatus.project.identifier)
            f = os.path.join(DOCBOX_DOC_ROOT, filename + '.copy')
            os.remove(f)
        except:
            pass

def apply_commit(commitString):
    copy_files_to_working_copy()
    delete_backup_files()
    # this occurs when changes have been committed
    docstates = DocStatus.objects.all()
    client = pysvn.Client()
    project = docstates[0].project.documentation_url.working_url
    def get_log_message():
        return True, "svn commit"
    client.callback_get_log_message = get_log_message
    client.checkin(project, commitString)
    docstates.delete()

def cancel_commit():
    for docstatus in DocStatus.objects.all():
        if docstatus.type == 'C':
            filename = format_string(docstatus.project.identifier)
            f = os.path.join(DOCBOX_DOC_ROOT, filename + '.html')
            os.remove(f)
            project = docstatus.project
            docstatus.delete()
            project.delete()
        elif docstatus.type == 'U':
            filename = format_string(docstatus.project.identifier)
            f = os.path.join(DOCBOX_DOC_ROOT, filename + '.html')
            c = os.path.join(DOCBOX_DOC_ROOT, filename + '.copy')
            shutil.copy(c, f)
            os.remove(c)
            docstatus.delete()
