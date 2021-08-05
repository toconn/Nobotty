from os import environ
from os import getcwd
from os.path import *
from platform import system


LINUX_SETTINGS_LOCATION = 'HOME'
WINDOWS_SETTINGS_LOCATION = 'HOMEPATH'


class Location:

    def __init__(self, settings_file_name, environment_name = None):
        if not settings_file_name:
            raise ValueError("Missing settings_file_name.")
        self.settings_file_name = settings_file_name
        self.environment_name = environment_name


def _default_directory_name(settings_location):
    return "." + splitext(basename(settings_location.settings_file_name))[0].lower()

def _default_location(settings_location, root_directory):
    return join(
        root_directory,
        _default_directory_name(settings_location),
        settings_location.settings_file_name)

def _in_current_directory(settings_location):
    return exists(current_directory_location(settings_location))

def _in_environment_location(settings_location):
    if not settings_location.environment_name:
        return False
    if settings_location.environment_name not in environ:
        return False
    return exists(environment_location(settings_location))

def _in_os_location(settings_location):
    return exists(os_location(settings_location))

def _is_windows_os():
    return system() == 'Windows'

def _linux_location(settings_location):
    return _default_location(settings_location, environ['HOME'])

def _windows_location(settings_location):
    return _default_location(settings_location, environ['HOMEPATH'])

def locate(settings_location):

    if _in_environment_location(settings_location):
        return environment_location(settings_location)

    if _in_os_location(settings_location):
        return os_location(settings_location)
        
    if _in_current_directory(settings_location):
        return current_directory_location(settings_location)

    raise FileNotFoundError(f"Could not find '{settings_location.settings_file_name}'")

def current_directory_location(settings_location):
    return join (getcwd(), settings_location.settings_file_name)

def environment_location(settings_location):
    return join(
        environ[settings_location.environment_name],
        settings_location.settings_file_name)

def os_location(settings_location):
    if _is_windows_os():
        return _windows_location(settings_location)
    return _linux_location(settings_location)

