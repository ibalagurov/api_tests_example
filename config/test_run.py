from . import env

API_TIMEOUT = env.get_int(key='API_TIMEOUT', default=30)
DEBUG = env.get_bool(key='DEBUG', default=False)
