from django.test.simple import DjangoTestSuiteRunner
import pdb
import traceback

try:
    # Django 1.3+
    from django.utils import unittest
except ImportError:
    # Django 1.2
    import unittest
    from django.test.simple import DjangoTestRunner
else:
    # Django 1.3+
    from django.utils.unittest import TextTestRunner as DjangoTestRunner

from django_pdb.utils import has_ipdb, get_ipdb


class ExceptionTestResultMixin(object):
    """
    A mixin class that can be added to any test result class.
    Drops into pdb on test errors/failures.
    """
    pdb_type = 'pdb'

    def get_pdb(self):
        if self.pdb_type == 'ipdb' and has_ipdb():
            import ipdb
            return ipdb
        return pdb

    def addError(self, test, err):
        super(ExceptionTestResultMixin, self).addError(test, err)
        exctype, value, tb = err

        self.stream.writeln()
        self.stream.writeln(self.separator1)
        self.stream.writeln(">>> %s" % (self.getDescription(test)))
        self.stream.writeln(self.separator2)
        self.stream.writeln(self._exc_info_to_string(err, test).rstrip())
        self.stream.writeln(self.separator1)
        self.stream.writeln()

        # Skip test runner traceback levels
        #while tb and self._is_relevant_tb_level(tb):
        #    tb = tb.tb_next

        self.get_pdb().post_mortem(tb)

    def addFailure(self, test, err):
        super(ExceptionTestResultMixin, self).addFailure(test, err)
        exctype, value, tb = err

        self.stream.writeln()
        self.stream.writeln(self.separator1)
        self.stream.writeln(">>> %s" % (self.getDescription(test)))
        self.stream.writeln(self.separator2)
        self.stream.writeln(self._exc_info_to_string(err, test).rstrip())
        self.stream.writeln(self.separator1)
        self.stream.writeln()

        ## Skip test runner traceback levels
        #while tb and self._is_relevant_tb_level(tb):
        #    tb = tb.tb_next

        # Really hacky way to jump up a couple of frames.
        # I'm sure it's not that difficult to do properly,
        # but I havn't figured out how.
        #p = pdb.Pdb()
        #p.reset()
        #p.setup(None, tb)
        #p.do_up(None)
        #p.do_up(None)
        #p.cmdloop()

        # It would be good if we could make sure we're in the correct frame here
        self.get_pdb().post_mortem(tb)


class PdbTestResult(ExceptionTestResultMixin, unittest.TextTestResult):
    pass


class PdbTestRunner(DjangoTestRunner):
    """
    Override the standard DjangoTestRunner to instead drop into pdb on test errors/failures.
    """
    def _makeResult(self):
        return PdbTestResult(self.stream, self.descriptions, self.verbosity)


class PdbTestSuiteRunner(DjangoTestSuiteRunner):
    """
    Override the standard DjangoTestSuiteRunner to instead drop into pdb on test errors/failures.
    """
    def run_suite(self, suite, **kwargs):
        return PdbTestRunner(verbosity=self.verbosity, failfast=self.failfast).run(suite)


class IPdbTestResult(ExceptionTestResultMixin, unittest.TextTestResult):

    pdb_type = 'ipdb'


class IPdbTestRunner(DjangoTestRunner):
    """
    Override the standard DjangoTestRunner to instead drop into ipdb on test errors/failures.
    """
    def _makeResult(self):
        return IPdbTestResult(self.stream, self.descriptions, self.verbosity)


class IPdbTestSuiteRunner(DjangoTestSuiteRunner):
    """
    Override the standard DjangoTestSuiteRunner to instead drop into ipdb on test errors/failures.
    """

    def run_suite(self, suite, **kwargs):
        return IPdbTestRunner(verbosity=self.verbosity, failfast=self.failfast).run(suite)

    