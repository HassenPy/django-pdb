import inspect
import os
import pdb
import sys
from django.core.exceptions import MiddlewareNotUsed


class PdbMiddleware(object):
    """
    Middleware to break into pdb at the start of views.

    If `always_break` is set, due to `runserver --pdb` this will break
    into pdb at the start of every view.

    Otherwise it will break into pdb at the start of the view if
    a 'pdb' GET parameter is set on the request url.
    """

    always_break = False
  
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        If running with '--pdb', set a breakpoint at the start
        of each of each view before it gets called.
        """
        
        # Skip out unless using `runserver --pdb`,
        # or `pdb` is in the command line parameters
        if not (self.always_break or 'pdb' in request.GET):
            return
 
        filename = inspect.getsourcefile(view_func)
        basename = os.path.basename(filename)
        dirname = os.path.basename(os.path.dirname(filename))
        lines, lineno = inspect.getsourcelines(view_func)
        temporary = True
        cond = None
        funcname = view_func.__name__

        print
        print '%s %s' % (request.method, request.get_full_path())
        print 'function "%s" in %s/%s:%d' % (funcname, dirname, basename, lineno)
        print 'args: %s' % (view_args,)
        print 'kwargs: %s' % (view_kwargs,)
        print

        p = pdb.Pdb()
        p.reset()
        p.set_break(filename, lineno, temporary, cond, funcname)
        sys.settrace(p.trace_dispatch)
