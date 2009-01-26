import os
import shutil
import codecs
from page import Page, url_to_filename
from settings import DOCBOX_DOC_ROOT
from docboxdata.data.models import Project, DocStatus

def format_string(title):
    return title.lower().replace(' ', '_')

def copyfile(project):
    filename = format_string(project.identifier)
    f = os.path.join(DOCBOX_DOC_ROOT, filename + '.html')
    c = os.path.join(DOCBOX_DOC_ROOT, filename + '.copy')
    shutil.copy(f, c)

def read_from_file(identifier):
    try:
        filename = format_string(identifier)
        f=codecs.open(os.path.join(DOCBOX_DOC_ROOT, filename + '.html'), 'r', 'utf-8')
        htmldata = f.read()
        f.close()
        return htmldata
    except:
        return ''

# page should be parsed and checked for template errors, template errors should be notified.
def write_to_file(contents, identifier):
    page = Page.from_string(contents)
    filename = format_string(identifier) + '.html'
    filepath = os.path.join(DOCBOX_DOC_ROOT, filename)

    path = os.path.dirname(filepath)
    if not os.path.exists(path):
        os.makedirs(path)

    f = codecs.open(filepath, 'w', 'utf-8')
    f.write(contents)
    f.close()
    return True #, page

    return False #, None
