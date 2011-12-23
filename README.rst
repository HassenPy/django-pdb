Django PDB
==========

Make debugging Django easier
----------------------------

Adding ``pdb.set_trace()`` to your source files every time you want to break into pdb sucks.

Don't do that.

Do this.

Installation
------------

Install using pip::

    pip install django-pdb

Add to your django project::

    INSTALLED_APPS = (
        ...
        'django_pdb',
    )

Usage
-----

``manage.py runserver``

Drops into pdb at the start of a view if the URL includes a `pdb` GET parameter.
Drops into ipdb at the start of a view if the URL includes a `ipdb` GET parameter.

Only enabled if ``settings.DEBUG = True``::

    bash: testproject/manage.py runserver
    Validating models...
    
    0 errors found
    Django version 1.3, using settings 'testproject.settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
    
    GET /test?pdb
    function "myview" in testapp/views.py:7
    args: ()
    kwargs: {}
    
    > /Users/tom/github/django-pdb/testproject/testapp/views.py(8)myview()
    -> a = 1
    (Pdb)

    GET /test?ipdb
    function "myview" in testapp/views.py:7
    args: ()
    kwargs: {}
    
    > /Users/tom/github/django-pdb/testproject/testapp/views.py(8)myview()
          7 def myview(request):
    3---> 8     a = 1
          9     b = 2
    ipdb>

``manage.py runserver --pdb`` or ``manage.py runserver --ipdb``

Drops into pdb or ipdb at the start of every view::

    bash: testproject/manage.py runserver --pdb
    Validating models...
    
    0 errors found
    Django version 1.3, using settings 'testproject.settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
    
    GET /test
    function "myview" in testapp/views.py:7
    args: ()
    kwargs: {}
    
    > /Users/tom/github/django-pdb/testproject/testapp/views.py(7)myview()
    -> a = 1
    (Pdb)

    bash: testproject/manage.py runserver --ipdb
    Validating models...
    
    0 errors found
    Django version 1.3, using settings 'testproject.settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
    
    GET /test
    function "myview" in testapp/views.py:7
    args: ()
    kwargs: {}
    
    > /Users/tom/github/django-pdb/testproject/testapp/views.py(8)myview()
          7 def myview(request):
    3---> 8     a = 1
          9     b = 2
    ipdb>


``manage.py test --pdb`` or ``manage.py test --ipdb``

Drops into pdb or ipdb on test errors/failures::

    bash: testproject/manage.py test testapp --pdb
    Creating test database for alias 'default'...
    E
    ======================================================================
    >>> test_error (testapp.tests.SimpleTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/Users/tom/github/django-pdb/testproject/testapp/tests.py", line 16, in test_error
        one_plus_one = four
    NameError: global name 'four' is not defined
    ======================================================================
    
    > /Users/tom/github/django-pdb/testproject/testapp/tests.py(16)test_error()
    -> one_plus_one = four
    (Pdb) 

    bash: testproject/manage.py test testapp --pdb
    Creating test database for alias 'default'...
    E
    ======================================================================
    >>> test_error (testapp.tests.SimpleTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/Users/tom/github/django-pdb/testproject/testapp/tests.py", line 16, in test_error
        one_plus_one = four
    NameError: global name 'four' is not defined
    ======================================================================
    
    > /Users/tom/github/django-pdb/testproject/testapp/tests.py(16)test_error()
          15         c = 3
     ---> 16         one_plus_one = four
          17 
     ipdb> 


Other apps that override runserver
--------------------------------------

If you also use other apps that override runserver, but still want to use `django_pdb`...

Add the following to your settings.py:

    if DEBUG:
        MIDDLEWARE_CLASSES += ('django_pdb.middleware.PdbMiddleware',)

Then, there is no need to have `django_pdb` in your INSTALLED_APPS, but you can still
add `pdb` to the URL query string.
