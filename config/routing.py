from . import env

BASE_URL = env.get(key='BASE_URL', default="https://cloud-api.yandex.net:443/v1")
VERIFY_SSL = env.get_bool(key='VERIFY_SSL', default=True)
