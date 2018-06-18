from functools import partial
from .. import http_session
from . import connector


def check_and_return_json(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        response.raise_for_status()
        return response.json()
    return wrapper


def custom_resources_response(method, by_user='authorized', **kwargs):
    request = connector.disk_resources(method=method, **kwargs)
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


def delete_resources(*args, **kwargs):
    response = delete_resources_response(*args, **kwargs)
    response.raise_for_status()
    return response


def custom_upload_resource_response(method, by_user='authorized', **kwargs):
    request = connector.disk_resource_upload(method=method, **kwargs)
    response = http_session.send_request(request=request, by_user=by_user)
    return response


get_upload_resource_response = partial(custom_upload_resource_response, method='get')
post_upload_resource_response = partial(custom_upload_resource_response, method='post')


@check_and_return_json
def get_upload_resource(*args, **kwargs):
    return get_upload_resource_response(*args, **kwargs)


@check_and_return_json
def post_upload_resource(*args, **kwargs):
    return post_upload_resource_response(*args, **kwargs)
