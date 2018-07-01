import pytest
import config
from testlib import helper
from testlib import check


@pytest.mark.parametrize('file_name, link, mime_type', [
    ('test_jpg.jpg', config.data.TEST_DATA_URL['test_jpg.jpg'], 'image/jpeg'),
    ('test_txt.txt', config.data.TEST_DATA_URL['test_txt.txt'], 'text/plain'),
])
def test_upload_file_with_type(base_folder, file_name, link, mime_type):
    """ Temporary folder is created, upload in it image, operation should be successful, file should be available and
        have expected name and mime type """
    file_path = f'{base_folder}/{file_name}'
    response = helper.post_upload_resource_response(params=dict(path=file_path, url=link))

    check.response_has_status_code(response, 202)
    check.response_has_fields(response, 'href')
    href = response.json().get('href')
    operation_id = href.split('/')[-1]

    helper.when_operation_status(operation_id, 'success')

    response = helper.get_resources_response(params=dict(path=file_path))
    check.response_has_status_code(response, 200)
    check.response_has_field_with_value(response, "mime_type", mime_type)
    check.response_has_field_with_value(response, "name", file_name)


def test_uploaded_file_with_same_name_should_have_postfix(base_folder):
    file_path = f'{base_folder}/same_name.txt'
    link = config.data.TEST_DATA_URL['test_txt.txt']
    helper.upload_and_wait_status(params=dict(path=file_path, url=link), status='success')
    helper.upload_and_wait_status(params=dict(path=file_path, url=link), status='success')

    response = helper.get_resources_response(params=dict(path=file_path))
    check.response_has_status_code(response, 200)
    check.response_has_field_with_value(response, "name", 'same_name.txt')

    response = helper.get_resources_response(params=dict(path=f'{base_folder}/same_name (1).txt'))
    check.response_has_status_code(response, 200)
    check.response_has_field_with_value(response, "name", 'same_name (1).txt')


def test_file_uploading_should_increase_used_space(base_folder):
    file_path = f'{base_folder}/used_space.txt'
    link = config.data.TEST_DATA_URL['test_txt.txt']

    space_before = helper.get_disk_info().get('used_space')

    helper.upload_and_wait_status(params=dict(path=file_path, url=link), status='success')

    space_after = helper.get_disk_info().get('used_space')

    assert space_after > space_before, "Used space wasn't changed after file uploading"


def test_upload_file_to_nonexistent_folder():
    link = config.data.TEST_DATA_URL['test_txt.txt']
    file_path = f'nonexistent_folder/existed_file.txt'
    response = helper.post_upload_resource_response(params=dict(path=file_path, url=link))

    check.response_has_status_code(response, 409)
    check.response_has_only_fields(response, 'message', 'description', 'error')
    check.response_has_field_with_value(response, field='error', value='DiskPathDoesntExistsError')


def test_upload_file_from_nonexistent_url(base_folder):
    link = config.data.TEST_DATA_URL['nonexistent_url']
    file_path = f'{base_folder}/from_nonexistent_url.txt'

    helper.upload_and_wait_status(params=dict(path=file_path, url=link), status='failed')


@pytest.mark.parametrize('fields', [
    ['href'], ['href', 'method'], ['href', 'method', 'templated']
])
def test_upload_file_and_get_existent_fields(base_folder, fields):
    link = config.data.TEST_DATA_URL['test_txt.txt']
    file_path = f'{base_folder}/fields_test{fields}.txt'
    response = helper.post_upload_resource_response(params=dict(path=file_path, url=link, fields=','.join(fields)))

    check.response_has_status_code(response, 202)
    check.response_has_only_fields(response, *fields)


def test_upload_file_by_unauthorized_user(base_folder):
    link = config.data.TEST_DATA_URL['test_txt.txt']
    file_path = f'{base_folder}/unauthorized.txt'
    response = helper.post_upload_resource_response(params=dict(path=file_path, url=link), by_user='unauthorized')

    check.response_has_status_code(response, 401)
    check.response_has_only_fields(response, 'message', 'description', 'error')
    check.response_has_field_with_value(response, field='error', value='UnauthorizedError')


@pytest.mark.parametrize('path,url', [
    (None, None),
    (None, 'valid'),
    ('valid', None)
])
def test_upload_file_with_invalid_params(path, url, base_folder):
    link = None if url is None else config.data.TEST_DATA_URL['test_txt.txt']
    file_path = None if path is None else f'{base_folder}/{url}{path}.txt'
    response = helper.post_upload_resource_response(params=dict(path=file_path, url=link))

    check.response_has_status_code(response, 400)
    check.response_has_only_fields(response, 'message', 'description', 'error')
    check.response_has_field_with_value(response, field='error', value='FieldValidationError')


def test_upload_file_with_empty_params():
    response = helper.post_upload_resource_response()

    check.response_has_status_code(response, 400)
    check.response_has_only_fields(response, 'message', 'description', 'error')
    check.response_has_field_with_value(response, field='error', value='FieldValidationError')
