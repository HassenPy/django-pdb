from django.core.management.commands.test import Command as TestCommand
from django_pdb.testrunners import PdbTestSuiteRunner
from django_pdb.testrunners import IPdbTestSuiteRunner
from optparse import make_option
import sys


class Command(TestCommand):
    """
    Identical to Django's standard 'test' management command,
    except that it also adds support for a '--pdb' option.
    """

    option_list = TestCommand.option_list + (
        make_option('--pdb', action='store_true', dest='pdb', default=False,
            help='Drop into pdb shell on test errors or failures.'),
        make_option('--ipdb', action='store_true', dest='ipdb', default=False,
            help='Drop into ipdb shell on test errors or failures.'),
    )

    pdb_testrunner = PdbTestSuiteRunner
    ipdb_testrunner = IPdbTestSuiteRunner

    def handle(self, *test_labels, **options):
        """
        If --pdb is set on the command line ignore the default test runner
        use the pdb test runner instead.
        """
        pdb = options.pop('pdb')
        ipdb = options.pop('ipdb')

        if pdb or ipdb:
            options['verbosity'] = int(options.get('verbosity', 1))

            if ipdb:
                test_runner = self.ipdb_testrunner(**options)
            else:
                test_runner = self.pdb_testrunner(**options)
            failures = test_runner.run_tests(test_labels)

            if failures:
                sys.exit(bool(failures))

        else:
            super(Command, self).handle(*test_labels, **options)
