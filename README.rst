Django PDB
==========

Adding `pdb.set_trace()` to your source files every time you want to break into pdb sucks.

Don't do that.

Do this.

Install using pip:

    pip install django-pdb

Add to your django project:

    INSTALLED_APPS = (
        ...
        'django_pdb',
    )

