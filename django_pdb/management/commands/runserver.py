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
        make_option('--ipdb', action='store_true', dest='ipdb', default=False,
            help='Drop into ipdb shell on at the start of any view.'),
    )

    def handle(self, *args, **options):
        # Add pdb middleware, if --pdb is specified, or if we're in DEBUG mode
        from django.conf import settings

        pdb_option = options.pop('pdb')
        ipdb_option = options.pop('ipdb')

        if pdb_option or settings.DEBUG:
            settings.MIDDLEWARE_CLASSES += ('django_pdb.middleware.PdbMiddleware',)

        # If --pdb is specified then always break at the start of views.
        # Otherwise break only if a 'pdb' query parameter is set in the url.
        if pdb_option:
            PdbMiddleware.always_break = 'pdb'
        elif ipdb_option:
            PdbMiddleware.always_break = 'ipdb'

        super(Command, self).handle(*args, **options)
