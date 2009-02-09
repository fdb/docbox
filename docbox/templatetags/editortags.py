from django import template
import datetime

register = template.Library()
def current_time(format_string="%Y-%m-%d %I:%M %p"):
    return datetime.datetime.now().strftime(str(format_string))
register.simple_tag(current_time)

def hello_world():
    return "Hello, World!"
register.simple_tag(hello_world)

@register.tag(name='startcode')
def do_code(parser, token):
    nodelist = parser.parse(('endcode',))
    parser.delete_first_token()
    return CodeNode(nodelist)

class CodeNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
    def render(self, context):
        from PyFontify import fontify
        output = unicode(self.nodelist.render(context))
        l = []
        s = 0
        for tag, start, end, li in fontify(output):
            if s < start:
                l.append(("", s, start))
            l.append((tag, start, end))
            s = end
        txt = ""
        for (tag, start, end) in l:
            if tag == "":
                txt += output[start:end]
            else:
                txt += '<span class="%s">%s</span>' % (tag, output[start:end])
        txt = '<div class="examplecode">%s</div>' % txt
        return txt

if __name__=='__main__':
    print "main"