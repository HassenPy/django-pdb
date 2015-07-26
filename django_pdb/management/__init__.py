import django
from django.core import management
from django.core.management import find_commands
if django.VERSION >= (1, 8):
    from importlib import import_module
else:
    from django.utils.importlib import import_module

from ..compat import load_management_modules

# A cache of loaded commands, so that call_command
# doesn't have to reload every time it's called.
_parent_commands = None


def get_parent_commands():
    """
    Returns a dictionary mapping command names to their callback applications.

    This function returns only callback applications above this
    application in the INSTALLED_APPS stack.
    """
    global _parent_commands
    if _parent_commands is None:
        django_path = management.__path__
        _parent_commands = dict([(name, 'django.core')
                                 for name in find_commands(django_path[0])])

        load_management_modules(_parent_commands)

        # Reset the Django management cache
        management._commands = None

    return _parent_commands


def load_parent_command(name):
    """
    Given a command name, returns the Command class instance that is
    the above the current application.

    (ImportError, AttributeError) are allowed to propagate.
    """
    app_name = get_parent_commands()[name]
    module = import_module('%s.management.commands.%s' % (app_name, name))
    return module.Command
