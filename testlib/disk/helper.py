from .. import http_session
from . import connector


def get_disk_info_response():
    request = connector.disk(method='get')
    return http_session.send_request(request=request)
