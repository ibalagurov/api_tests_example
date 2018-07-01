import pytest
import requests
from testlib import helper
from testlib import check


@pytest.fixture(scope='module')
def module_file(temp_file):
    path, file_name = temp_file()
    return path, file_name


@pytest.fixture(scope='module')
def module_folder(temp_folder):
    path, folder_name = temp_folder()
    return path, folder_name


def test_publish_file(module_file):
    file_path, file_name, *_ = module_file

    response = helper.put_publish_resource_response(params=dict(path=file_path))

    check.response_has_status_code(response, 200)
    check.response_has_only_fields(response, 'href', 'method', 'templated')
    check.response_has_field_contains_value(response, 'href', file_name)

    items = helper.get_public_resources().get('items')
    items_by_name = [item for item in items if item.get('name') == file_name]
    assert len(items_by_name) == 1

    response = requests.get(url=items_by_name[0]['file'])
    assert response.status_code == 200, 'Unable to get published file'


def test_publish_folder(module_folder):
    folder_path, folder_name, *_ = module_folder

    response = helper.put_publish_resource_response(params=dict(path=folder_path))

    check.response_has_status_code(response, 200)
    check.response_has_only_fields(response, 'href', 'method', 'templated')
    check.response_has_field_contains_value(response, 'href', folder_name)

    items = helper.get_public_resources().get('items')
    items_by_name = [item for item in items if item.get('name') == folder_name]
    assert len(items_by_name) == 1

    response = requests.get(url=items_by_name[0]['public_url'])
    assert response.status_code == 200, 'Unable to get published folder'


def test_publish_file_by_unauthorized_user(module_file):
    file_path, file_name, *_ = module_file

    response = helper.put_publish_resource_response(params=dict(path=file_path), by_user='unauthorized')

    check.response_has_status_code(response, 401)
    check.response_has_only_fields(response, 'message', 'description', 'error')
    check.response_has_field_with_value(response, field='error', value='UnauthorizedError')


def test_publish_folder_by_expired_user(module_folder):
    folder_path, folder_name, *_ = module_folder

    response = helper.put_publish_resource_response(params=dict(path=folder_path), by_user='expired')

    check.response_has_status_code(response, 401)
    check.response_has_only_fields(response, 'message', 'description', 'error')
    check.response_has_field_with_value(response, field='error', value='UnauthorizedError')


def test_publish_nonexistent_file():
    response = helper.put_publish_resource_response(params=dict(path='nonexistent_file'))

    check.response_has_status_code(response, 404)
    check.response_has_only_fields(response, 'message', 'description', 'error')
    check.response_has_field_with_value(response, field='error', value='DiskNotFoundError')


def test_publish_and_filter_fields(module_folder):
    folder_path, folder_name, *_ = module_folder

    response = helper.put_publish_resource_response(params=dict(path=folder_path, fields='href,method'))

    check.response_has_status_code(response, 200)
    check.response_has_only_fields(response, 'href', 'method')
