from django import template
import datetime

register = template.Library()
def current_time(format_string="%Y-%m-%d %I:%M %p"):
    return datetime.datetime.now().strftime(str(format_string))
register.simple_tag(current_time)

def hello_world():
    return "Hello, World!"
register.simple_tag(hello_world)