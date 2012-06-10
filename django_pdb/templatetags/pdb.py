from django import template
from django_pdb.utils import has_ipdb


register = template.Library()

@register.filter 
def pdb(element):
    if has_ipdb():
        from ipdb import set_trace
    else:
        from pdb import set_trace
    set_trace()
    return element
