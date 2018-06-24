from requests import Request
from functools import partial
from . import http_session
from config.routing import BASE_URL


def check_and_return_json(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        response.raise_for_status()
        return response.json()
    return wrapper


DISK_URL = BASE_URL + '/disk'
DISK_OPERATIONS_URL = BASE_URL + '/disk/operations'
DISK_RESOURCES_URL = BASE_URL + '/disk/resources'
DISK_RESOURCE_UPLOAD_URL = BASE_URL + '/disk/resources/upload'
DISK_RESOURCE_PUBLISH_URL = BASE_URL + '/disk/resources/publish'


# DISK
def custom_disk_response(method, by_user='authorized', **kwargs):
    request = Request(method=method, url=DISK_URL, **kwargs)
    response = http_session.send_request(request=request, by_user=by_user)
    return response


get_disk_info_response = partial(custom_disk_response, method='get')


# OPERATIONS
def custom_operations_response(method, operation_id, by_user='authorized', **kwargs):
    request = Request(method=method, url=f'{DISK_OPERATIONS_URL}/{operation_id}', **kwargs)
    response = http_session.send_request(request=request, by_user=by_user)
    return response


@check_and_return_json
def get_operation(operation_id):
    return custom_operations_response(method='get', operation_id=operation_id)


def operation_status(operation_id):
    return get_operation(operation_id).get('status')


# RESOURCES
# # Disk
def custom_resources_response(method, by_user='authorized', **kwargs):
    request = Request(method=method, url=DISK_RESOURCES_URL, **kwargs)
    response = http_session.send_request(request=request, by_user=by_user)
    return response


get_resources_response = partial(custom_resources_response, method='get')
put_resources_response = partial(custom_resources_response, method='put')
delete_resources_response = partial(custom_resources_response, method='delete')


@check_and_return_json
def get_resources(*args, **kwargs):
    return get_resources_response(*args, **kwargs)


@check_and_return_json
def put_resources(*args, **kwargs):
    return put_resources_response(*args, **kwargs)


@check_and_return_json
def delete_resources(*args, **kwargs):
    return delete_resources_response(*args, **kwargs)


# # Upload
def custom_upload_resource_response(method, by_user='authorized', **kwargs):
    request = Request(method=method, url=DISK_RESOURCE_UPLOAD_URL, **kwargs)
    response = http_session.send_request(request=request, by_user=by_user)
    return response


get_upload_resource_response = partial(custom_upload_resource_response, method='get')
post_upload_resource_response = partial(custom_upload_resource_response, method='post')


# # Publish
disk_resource_publish = partial(Request, url=DISK_RESOURCE_PUBLISH_URL)
