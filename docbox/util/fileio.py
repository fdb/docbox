import os
import codecs

def read_from_file(path):
    try:
        f=codecs.open(path, 'r', 'utf-8')
        htmldata = f.read()
        f.close()
        return htmldata
    except:
        return ''

def write_to_file(path, contents):
    try:
        f = codecs.open(path, 'w', 'utf-8')
        f.write(contents)
        f.close()
    except:
        raise
