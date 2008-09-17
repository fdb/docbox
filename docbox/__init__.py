#!/usr/bin/env python
import os
import shutil
from django.conf import settings
from django.template import Template, Context
from django.template.loader import get_template

def _handle_file(src_file, dst_file):
    print src_file
    contents = open(src_file).read()
    wrapped_contents = '{%% extends "base.html" %%}\n{%% load docbox %%}\n{%% block content %%}\n%s\n{%% endblock %%}' % contents
    template = Template(wrapped_contents)
    context = Context({'MEDIA_URL':settings.MEDIA_URL})
    html = template.render(context)
    try:
        os.makedirs(os.path.dirname(dst_file))
    except OSError, err:
        if err.errno != 17: # 'file exists' error is to be expected
            raise err
    open(dst_file, 'w').write(html)

def build_documentation(doc_dir, build_dir, template_dir=None, static_dir=None):
    if template_dir is None:
        template_dir = os.path.join(doc_dir, '_templates')
    if static_dir is None:
        static_dir = os.path.join(doc_dir, '_static')

    # Configure Django
    settings.configure(DEBUG=True, 
                       TEMPLATE_DEBUG=True, 
                       TEMPLATE_DIRS=(template_dir,),
                       INSTALLED_APPS=('docbox',),
                       MEDIA_URL='_static')

    # Walk the documentation
    for root, dirs, files in os.walk(doc_dir):
        if root in (template_dir, static_dir):
            continue
        for file in files:
            fname, ext = os.path.splitext(file)
            if ext == '.html':
                src_file = os.path.join(root, file)
                dst_file = os.path.join(build_dir, file)
                _handle_file(src_file, dst_file)

    # Copy over the static resources
    try:
        shutil.copytree(static_dir, os.path.join(build_dir, '_static'))
    except OSError, err:
        if err.errno != 17: # 'file exists' error is to be expected
            raise err
    
if __name__=='__main__':
    import sys
    sys.path.append('..')
    build_documentation('../docs', '../build/html')