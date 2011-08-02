from django.core.management.commands.runserver import Command as RunServerCommand
from django_pdb.middleware import PdbMiddleware
from optparse import make_option

class Command(RunServerCommand):
    """
    Identical to Django's standard 'runserver' management command,
    except that it also adds support for a '--pdb' option.
    """
    option_list = RunServerCommand.option_list + (
        make_option('--pdb', action='store_true', dest='pdb', default=False,
            help='Drop into pdb shell on at the start of any view.'),
    )

    def handle(self, *args, **options):
        # Add pdb middleware
        from django.conf import settings
        settings.MIDDLEWARE_CLASSES += ('django_pdb.middleware.PdbMiddleware',)
        
        # If --pdb is specified then always break at the start of views.
        # Otherwise break only if a 'pdb' query parameter is set in the url.  
        if options.pop('pdb'):
            PdbMiddleware.always_break = True

        super(Command, self).handle(*args, **options)
