import re
from django import template
from django.utils.html import mark_safe

register = template.Library()

def highlight(value, keyword):
    regex = re.compile(keyword, re.IGNORECASE)
    return mark_safe(regex.sub(f'<span class="highlight">{keyword}</span>',value))

register.filter('highlight',highlight)