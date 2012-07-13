from optparse import make_option
import sys

from django.core.management.commands import test

from django_pdb.management import load_parent_command
from django_pdb.testrunners import make_suite_runner


# Provide a Command class so that Django knows what will handle
# things. This module does not override it, so it just needs to find
# the parent Command.
Command = load_parent_command('test')


def patch_test_command(Command):
    """
    Monkeypatches Django's TestCommand so that it chooses to use
    ipdb or pdb, allowing subclasses to inherit from it and wrap its
    behaviour.
    """
    Command.option_list += type(Command.option_list)([
        make_option('--pdb', action='store_true', dest='pdb', default=False,
                    help='Drop into pdb shell on test errors or failures.'),
        make_option('--ipdb', action='store_true', dest='ipdb', default=False,
                    help='Drop into ipdb shell on test errors or failures.'),
    ])

    def handle(self, *test_labels, **options):
        """
        If --pdb is set on the command line ignore the default test runner
        use the pdb test runner instead.
        """
        pdb = options.pop('pdb')
        ipdb = options.pop('ipdb')

        if pdb or ipdb:
            options['verbosity'] = int(options.get('verbosity', 1))
            options['interactive'] = options.get('interactive', True)
            options['failfast'] = options.get('failfast', False)

            TestRunner = self.get_runner(use_ipdb=ipdb)
            test_runner = TestRunner(**options)
            failures = test_runner.run_tests(test_labels)

            if failures:
                sys.exit(bool(failures))

        else:
            self._handle(*test_labels, **options)

    Command._handle = Command.handle
    Command.handle = handle

    def get_runner(self, use_ipdb, suite_runner=None):
        return make_suite_runner(use_ipdb=use_ipdb, suite_runner=suite_runner)

    Command.get_runner = get_runner

patch_test_command(test.Command)
