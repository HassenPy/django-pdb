import inspect
import os
import pdb
import sys
from django.core.exceptions import MiddlewareNotUsed


class PdbMiddleware(object):
    """
    Middleware to break into pdb at the start of every view.
    """

    #enabled = False

    #def __init__(self):
    #    """
    #    Remove this middleware on startup if '--pdb' is not being used.
    #    """
    #    if not self.enabled:
    #        raise MiddlewareNotUsed
  
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        If running with '--pdb', set a breakpoint at the start
        of each of each view before it gets called.
        """
        filename = inspect.getsourcefile(view_func)
        basename = os.path.basename(filename)
        dirname = os.path.basename(os.path.dirname(filename))
        lines, lineno = inspect.getsourcelines(view_func)
        temporary = True
        cond = None
        funcname = view_func.__name__

        print
        print '%s %s' % (request.method, request.path)
        print 'function "%s" in %s/%s:%d' % (funcname, dirname, basename, lineno)
        print 'args: %s' % (view_args,)
        print 'kwargs: %s' % (view_kwargs,)
        print

        p = pdb.Pdb()
        p.reset()
        p.set_break(filename, lineno, temporary, cond, funcname)
        sys.settrace(p.trace_dispatch)
