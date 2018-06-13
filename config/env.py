import os


def get(key, default=None):
    return os.environ.get(key=key, default=default)


def get_bool(key, default):
    value = get(key, default)
    return str(value).lower() == 'true'


def get_int(key, default):
    value = get(key, default)
    return int(value)
