from .. import http_session
from . import connector


def get_disk_info_response():
    request = connector.disk(method='get')
    return http_session.send_request(request=request)


def get_disk_info():
    response = get_disk_info_response()
    response.raise_for_status()
    return response.json()
