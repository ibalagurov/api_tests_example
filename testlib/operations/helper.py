from .. import http_session
from . import connector


def custom_operations_response(method, operation_id, by_user='authorized', **kwargs):
    request = connector.disk_operations(method=method, operation_id=operation_id, **kwargs)
    response = http_session.send_request(request=request, by_user=by_user)
    return response


def get_operation_response(operation_id):
    return custom_operations_response(method='get', operation_id=operation_id)


def get_operations_status(operation_id):
    response = get_operation_response(operation_id=operation_id)
    response.raise_for_status()
    return response.json().get('status')
