from django.conf import settings
__version__ = '0.3.2'

POST_MORTEM = getattr(settings, 'POST_MORTEM', False)
DEBUG = getattr(settings, 'DEBUG', False)

if DEBUG and POST_MORTEM == True:
    from django.views import debug
    def runpdb(request, exc_type, exc_value, tb):
        import sys
        try:
            import ipdb
        except ImportError:
            import pdb as ipdb
        p = ipdb
        print >> sys.stderr, "Exception occured: %s, %s" % (exc_type, exc_value)
        p.post_mortem(tb)
    debug.technical_500_response = runpdb
