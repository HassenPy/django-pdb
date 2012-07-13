from django.core import management
from django.core.management import find_commands, find_management_module
from django.utils.importlib import import_module


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

        # Find the installed apps
        try:
            from django.conf import settings
            apps = settings.INSTALLED_APPS
        except (AttributeError, EnvironmentError, ImportError):
            apps = []

        # Find and load the management module for each installed app above
        # this one.
        for app_name in apps:
            try:
                path = find_management_module(app_name)
                if path == __path__[0]:
                    # Found this app
                    break

                _parent_commands.update(
                    dict([(name, app_name) for name in find_commands(path)])
                )
            except ImportError:
                pass  # No management module - ignore this app

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
