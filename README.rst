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

Add to your settings.py::

    # Make sure to add django_pdb before any apps that override the 'runserver'
    # or 'test' commands (Includes south and django.contrib.staticfiles)
    INSTALLED_APPS = (
        ...
        'django_pdb',
        ...
    )

    # After your MIDDLEWARE classes:
    if DEBUG:
        MIDDLEWARE_CLASSES += ('django_pdb.middleware.PdbMiddleware',)

Usage
-----

``manage.py runserver``

Drops into pdb at the start of a view if the URL includes a `pdb` GET parameter.

Drops into ipdb at the start of a view if the URL includes a `ipdb` GET parameter.

This behavior is only enabled if ``settings.DEBUG = True``::

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

``manage.py runserver --pdb`` **or** ``manage.py runserver --ipdb``

Drops into pdb/ipdb at the start of every view::

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


``manage.py test --pdb`` **or** ``manage.py test --ipdb``

Drops into pdb/ipdb on test errors/failures::

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


Post mortem mode
----------------

``manage.py runserver --pm``

Post mortem mode, drops into (i)pdb if an exception is raised in a view. This works only if there is
no other app overriding ``runserver`` command.

``POST_MORTEM = True``

You can also add ```POST_MORTEM = True``` to your ```settings.py``` to enable this option even if other app overrides ```runserver```.

Filter
------

You can also use the template filter ``pdb`` to explore a template viriable in (i)pdb this way::

    {% load pdb %}

    {{ variable|pdb }}

Example::

    bash: testproject/manage.py runserver
    Validating models...

    0 errors found
    Django version 1.4, using settings 'testproject.settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
    > /Users/tom/github/django-pdb/django_pdb/templatetags/pdb_filters.py(14)pdb()
    -> return element
    (Pdb) element
    "I'm the variable"
    (Pdb) element = "another value"
    (Pdb) c
    [11/May/2012 11:22:53] "GET /filter/ HTTP/1.1" 200 37

Other apps that override ``test``/``runserver``
-----------------------------------------------

``manage.py test --pdb`` **does not yet work** if you also have other apps that
override the ``test`` command.

``manage.py runserver --pdb`` **does not yet work** if you also have other apps
that override the ``runserver`` command.

Adding ``?pdb`` to the URL **does work** even if you have other apps that
override the ``runserver`` command.

Make sure to put ``django_pdb`` before any conflicting apps in
``INSTALLED_APPS`` so that they have priority.

Notable apps include ``django.contrib.staticfile`` and ``south``.
