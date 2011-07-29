from django.core.management.commands.runserver import Command as RunServerCommand
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
        if options.pop('pdb'):
            from django.conf import settings
            settings.MIDDLEWARE_CLASSES += ('django_pdb.middleware.PdbMiddleware',)
        super(Command, self).handle(*args, **options)
