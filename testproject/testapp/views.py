"""
A dummy view to demonstrate using 'manage.py runserver --pdb'
"""
from django.http import HttpResponse

def myview(request):
    a = 1
    b = 2
    c = 3
    return HttpResponse('Hello, you.', content_type='text/plain')
