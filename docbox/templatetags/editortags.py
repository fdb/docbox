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
        tags = fontify(output)
        html = output
        d = 0
        for tag, start, end, sublist in tags:
            html = html[:start+d] + """<span class="%s">%s</span>""" % (tag, html[start+d:end+d]) + html[end+d:]
            d += len(tag) + 22 # 22 is the length of the span HTML code
        return html

if __name__=='__main__':
    print "main"