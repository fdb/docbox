import re
import os

from django import template
from django.conf import settings

from django.template import Context, Template, RequestContext

def url_to_filename(url):
    return os.path.join(settings.DOCBOX_DOC_ROOT, url) + '.html'
    
def read_file(fname):
    html_as_ascii = open(fname).read()
    print type(html_as_ascii)
    assert(type(html_as_ascii) is str)
    html = html_as_ascii.decode('utf-8')
    assert(type(html) is unicode)
    return html

def read_url(url):
    return read_file(url_to_filename(url))

META_TAG_START = '<!--'
META_TAG_END = '-->'
meta_re = re.compile('(%s\s*![a-zA-Z]+\s*\:.*?%s)' % (re.escape(META_TAG_START), re.escape(META_TAG_END)))
meta_inner_re = re.compile('!([a-zA-Z]+)\s*\:\s*(.*)')

class MetaParser(object):
    def __init__(self, html):
        self.html = html
        self.attributes = {}
        
    def parse(self):
        for bit in meta_re.split(self.html):
            if not bit: continue
            if bit.startswith(META_TAG_START):
                inner = bit[len(META_TAG_START):-len(META_TAG_END)].strip()
                match = meta_inner_re.search(inner)
                key, value = match.groups()
                self.attributes[key] = value

class Page(object):
    """A Page contains the contents and meta-information of a HTML document."""
    
    def __init__(self, html, title=None):
        self.html = html
        self.title = title
        
    def from_string(cls, html):
        """Parse a page from a HTML string."""
        parser = MetaParser(html)
        parser.parse()
        title = parser.attributes.pop('title', None)
        return Page(html, title)
    from_string=classmethod(from_string)

    def from_url(cls, url):
        """Parse a page from a given relative URL.
        
        This does not load the page from an external resource,
        but only works for internal URLs."""
        return cls.from_string(read_url(url))
    from_url=classmethod(from_url)

    def from_file(cls, fname):
        """Parse a page from a file."""
        return cls.from_string(read_file(fname))
    from_file=classmethod(from_file)
    
    def render(self, request=None):
        """Render the contents of the page."""
        # Prefix html with internal loads
        html = '''{%% load docbox %%}%s''' % self.html
        t = Template(html)
        if request is None:
            ctx = Context()
        else:
            ctx = RequestContext(request)
        ctx['page'] = self
        return t.render(ctx)

if __name__=='__main__':
    import sys
    sys.path.append('..')
    # Needed for Django
    settings.configure(INSTALLED_APPS=('docbox',))
    html = '''<!-- !title: Title of the page -->
<p>{% hello_world %}</p>
<p>{% current_time %}</p>
'''
    page = Page.from_string(html)
    print page.render()