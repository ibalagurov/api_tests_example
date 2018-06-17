from functools import partial
from .. import http_session
from . import connector


def custom_disk_response(method, by_user='authorized', **kwargs):
    request = connector.disk(method=method, **kwargs)
    response = http_session.send_request(request=request, by_user=by_user)
    return response


get_disk_info_response = partial(custom_disk_response, method='get')


def get_disk_info():
    response = get_disk_info_response()
    response.raise_for_status()
    return response.json()
