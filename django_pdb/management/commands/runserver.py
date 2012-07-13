import sys
import pdb

from django_pdb.management import load_parent_command
from django_pdb.middleware import PdbMiddleware

from optparse import make_option
from django_pdb.utils import has_ipdb
from django.views import debug


RunServerCommand = load_parent_command('runserver')


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
        make_option('--pm', action='store_true', dest='pm', default=False,
            help='Drop into ipdb shell if an exception is raised in a view.'),
    )

    def handle(self, *args, **options):
        # Add pdb middleware, if --pdb is specified, or if we're in DEBUG mode
        from django.conf import settings

        pdb_option = options.pop('pdb')
        ipdb_option = options.pop('ipdb')

        middleware = 'django_pdb.middleware.PdbMiddleware'
        if ((pdb_option or settings.DEBUG)
            and middleware not in settings.MIDDLEWARE_CLASSES):
            settings.MIDDLEWARE_CLASSES += (middleware,)

        self.pm = options.pop('pm')
        if self.pm:
            debug.technical_500_response = self.reraise

        # If --pdb is specified then always break at the start of views.
        # Otherwise break only if a 'pdb' query parameter is set in the url.
        if pdb_option:
            PdbMiddleware.always_break = 'pdb'
        elif ipdb_option:
            PdbMiddleware.always_break = 'ipdb'

        super(Command, self).handle(*args, **options)

    def reraise(self, request, exc_type, exc_value, tb):
        if has_ipdb():
            import ipdb
            p = ipdb
        else:
            p = pdb
        if self.pm:
            print >>sys.stderr, "Exception occured: %s, %s" % (exc_type, exc_value)
            p.post_mortem(tb)
        else:
            raise
