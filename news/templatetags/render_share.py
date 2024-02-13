
from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag
def render_share(src_template, item):
    return render_to_string('pages/share/' + src_template, {'item':item})

