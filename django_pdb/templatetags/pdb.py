from django import template
from django_pdb.utils import has_ipdb, has_pudb


register = template.Library()

@register.filter
def pdb(element):
    from django_pdb.utils import get_pdb_set_trace
    get_pdb_set_trace()()
    return element


@register.filter
def ipdb(element):
    if has_ipdb():
        from ipdb import set_trace
    else:
        from django_pdb.utils import get_pdb_set_trace
        get_pdb_set_trace()()
    set_trace()
    return element

@register.filter
def pudb(element):
    if has_pudb():
        from pudb import set_trace
    else:
        from django_pdb.utils import get_pdb_set_trace
        get_pdb_set_trace()()
    set_trace()
    return element
