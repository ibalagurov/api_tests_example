from requests import Request
from functools import partial
from . import http_session
from waiting import wait
from config.routing import BASE_URL


# COMMON
def check_and_return_json(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        response.raise_for_status()
        return response.json()
    return wrapper


def check_and_return_text(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        response.raise_for_status()
        return response.text
    return wrapper


def send_request_and_get_response(func):
    def wrapper(by_user='authorized', *args, **kwargs):
        request = func(*args, **kwargs)
        response = http_session.send_request(request=request, by_user=by_user)
        return response
    return wrapper


def get_operation_id_from_response(response):
    json = response.json()
    operation_id = get_operation_id_from_json(json)
    return operation_id


def get_operation_id_from_json(json):
    href = json.get('href')
    assert href
    operation_id = href.split('/')[-1]
    return operation_id


# ENDPOINTS
DISK_URL = BASE_URL + '/disk'
DISK_OPERATIONS_URL = BASE_URL + '/disk/operations'
DISK_RESOURCES_URL = BASE_URL + '/disk/resources'
DISK_PUBLIC_RESOURCES_URL = BASE_URL + '/disk/resources/public/'
DISK_RESOURCE_UPLOAD_URL = BASE_URL + '/disk/resources/upload'
DISK_RESOURCE_PUBLISH_URL = BASE_URL + '/disk/resources/publish'


# DISK
@send_request_and_get_response
def custom_disk_response(method, **kwargs):
    return Request(method=method, url=DISK_URL, **kwargs)


get_disk_info_response = partial(custom_disk_response, method='get')


@check_and_return_json
def get_disk_info():
    return get_disk_info_response()


# OPERATIONS
@send_request_and_get_response
def custom_operations_response(method, operation_id, **kwargs):
    return Request(method=method, url=f'{DISK_OPERATIONS_URL}/{operation_id}', **kwargs)


@check_and_return_json
def get_operation(operation_id):
    return custom_operations_response(method='get', operation_id=operation_id)


def operation_status(operation_id):
    return get_operation(operation_id).get('status')


def when_operation_status(operation_id, status):
    wait(
        predicate=lambda: operation_status(operation_id=operation_id) == status,
        timeout_seconds=30, sleep_seconds=(1, 2, 4)
    )


# RESOURCES
# # Disk
@send_request_and_get_response
def custom_resources_response(method, **kwargs):
    return Request(method=method, url=DISK_RESOURCES_URL, **kwargs)


get_resources_response = partial(custom_resources_response, method='get')
put_resources_response = partial(custom_resources_response, method='put')
delete_resources_response = partial(custom_resources_response, method='delete')


@check_and_return_json
def get_resources(*args, **kwargs):
    return get_resources_response(*args, **kwargs)


@check_and_return_json
def put_resources(*args, **kwargs):
    return put_resources_response(*args, **kwargs)


create_folder = put_resources


@check_and_return_text
def delete_resources(*args, **kwargs):
    return delete_resources_response(*args, **kwargs)


def safe_delete(path):
    response = delete_resources_response(params={'path': path})
    code = response.status_code
    assert code in [202, 204, 404]  # 404 - means that parent folder was deleted
    if code == 202:
        # for exclude resource blocking in async deleting nested resources
        operation_id = get_operation_id_from_response(response)
        when_operation_status(operation_id=operation_id, status='success')


# # Upload
@send_request_and_get_response
def custom_upload_resource_response(method, **kwargs):
    return Request(method=method, url=DISK_RESOURCE_UPLOAD_URL, **kwargs)


get_upload_resource_response = partial(custom_upload_resource_response, method='get')
post_upload_resource_response = partial(custom_upload_resource_response, method='post')


@check_and_return_json
def post_upload_resource(*args, **kwargs):
    return post_upload_resource_response(*args, **kwargs)


def upload_and_wait_status(status, *args, **kwargs):
    json = post_upload_resource(*args, **kwargs)
    href = json.get('href')
    assert href
    operation_id = href.split('/')[-1]
    when_operation_status(operation_id=operation_id, status=status)


# # Publish
@send_request_and_get_response
def custom_publish_resource_response(method, **kwargs):
    return Request(method=method, url=DISK_RESOURCE_PUBLISH_URL, **kwargs)


put_publish_resource_response = partial(custom_publish_resource_response, method='put')


@check_and_return_json
def put_publish_resource(*args, **kwargs):
    return put_publish_resource_response(*args, **kwargs)


# # Public
@send_request_and_get_response
def custom_public_resource_response(method, **kwargs):
    return Request(method=method, url=DISK_PUBLIC_RESOURCES_URL, **kwargs)


get_public_resources_response = partial(custom_public_resource_response, method='get')


@check_and_return_json
def get_public_resources(*args, **kwargs):
    return get_public_resources_response(*args, **kwargs)