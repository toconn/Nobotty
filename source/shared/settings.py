from os.path import expandvars


COMMENT_INDICATOR = '#'
SEPARATOR_1 = '='
SEPARATOR_2 = '\t'


## File - Read ##############################################

def _is_split_with(line, separator):

    location = line.find(separator)
    return 0 < location < len(line) - 1


def _is_comment(line: str) -> bool:
    return line.startswith(COMMENT_INDICATOR)


def _is_empty(line: str) -> bool:
    return not line


def _is_setting(line: str) -> bool:
    """ Return true if has separator and it isn't
        the first or last character.
    """
    if _is_comment(line) or \
            _is_empty(line):
        return False

    return (
        _is_split_with(line, SEPARATOR_1) or
        _is_split_with(line, SEPARATOR_2))


def _normalize_key(value):
    return value.strip()


def _normalize_line(value):
    return value.strip()


def _normalize_value(value):

    if "$" in value:
        value = expandvars(value)

    return value.strip()


def _not_found(self, index, search):
    """ Tests whether a match was found
        after a string find.
    """
    return index == -1


def _to_key_value(line: str) -> ():

    if SEPARATOR_1 in line:
        key, value = line.split(SEPARATOR_1, 1)
    else:
        key, value = line.split(SEPARATOR_2, 1)

    key = _normalize_key(key)
    value = _normalize_value(value)

    return key, value


def read_to_dict(file_path):

    settings = {}

    with open(file_path, "rt") as file:

        for line in file:
            if line:
                line = _normalize_line (line)
                if _is_setting(line):
                    key, value = _to_key_value(line)
                    settings[key] = value
            else:
                break

    return settings


## Validation ##############################################

def validate(settings, required_settings):
        """ Validates that the configuration
            contains all the required sections
            and properties.
        """
        errors = []

        for name in required_settings:
            if name not in settings:
                errors.append(f"Setting '{name}' is missing.")

        if errors:
            raise ValueError('\n'.join(errors))


## Settings ################################################

class Settings:

    def __init__(self, file_path = None):

        if file_path:
            self.read(file_path)
        else:
            self._settings = {}


    def __contains__(self, name):
        return self._has(name)


    def get(self, name, default = None):
        return self._settings.get (name, default)


    def get_boolean(self, name, default = False):

        if not self._has(name):
            return default

        value = self.get(name).lower()

        if value in ('true', 't', 'yes', 'y', 'on', '1'):
            return True

        if value in ('false', 'f', 'no', 'n', 'off', '0'):
            return False

        raise InvalidValue (f"{name}: Can't convert '{value}' to boolean.")


    def get_float(self, name, default = 0.0):
        return float (self.get (name, default))


    def get_int(self, name, default = 0):
        return int (self.get (name, default))


    def read(self, file_path):
        self._settings = read_to_dict(file_path)


    def validate(self, required_settings):
        """ Validates that the configuration
            contains all the required sections
            and properties.
        """
        errors = []

        for name in required_settings:
            if not self._has(name):
                errors.append(f"Setting '{name}' is missing.")

        if errors:
            raise ValueError('\n'.join(errors))


    def _has(self, name):
        return name in self._settings

