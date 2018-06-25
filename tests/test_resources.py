import pytest
from testlib import helper
from testlib import check


_TEST_DATA_URL = 'https://github.com/ibalagurov/api_tests_example/blob/master/test_data'


@pytest.mark.parametrize('file_name, link, mime_type', [
    ('test_jpg.jpg', f'{_TEST_DATA_URL}/test_jpg.jpg', 'image/jpeg'),
    ('test_txt.txt', f'{_TEST_DATA_URL}/test_txt.txt', 'text/plain'),
])
def test_upload_file_with_type(temp_folder, file_name, link, mime_type):
    """ Temporary folder is created, upload in it image, operation should be successful, file should be available and
        have expected name and mime type """
    file_path = f'{temp_folder}/{file_name}'
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


def test_uploaded_file_with_same_name_should_have_postfix(temp_folder):
    file_path = f'{temp_folder}/same_name.txt'
    link = f'{_TEST_DATA_URL}/test_txt.txt'
    helper.upload_and_wait_status(params=dict(path=file_path, url=link), status='success')
    helper.upload_and_wait_status(params=dict(path=file_path, url=link), status='success')

    response = helper.get_resources_response(params=dict(path=file_path))
    check.response_has_status_code(response, 200)
    check.response_has_field_with_value(response, "name", 'same_name.txt')

    response = helper.get_resources_response(params=dict(path=f'{temp_folder}/same_name (1).txt'))
    check.response_has_status_code(response, 200)
    check.response_has_field_with_value(response, "name", 'same_name (1).txt')


def test_upload_file_to_nonexistent_folder():
    link = f'{_TEST_DATA_URL}/test_txt.txt'
    file_path = f'unexistent_folder/existed_file.txt'
    response = helper.post_upload_resource_response(params=dict(path=file_path, url=link))

    check.response_has_status_code(response, 409)
    check.response_has_field_with_value(response, field='error', value='DiskPathDoesntExistsError')
    check.response_does_not_have_fields(response, 'href')


def test_upload_file_from_nonexistent_url(temp_folder):
    link = f'{_TEST_DATA_URL}/nonexistent_url.txt'
    file_path = f'{temp_folder}/from_nonexistent_url.txt'

    helper.upload_and_wait_status(params=dict(path=file_path, url=link), status='failed')


@pytest.mark.parametrize('fields', [
    ['href'], ['href', 'method'], ['href', 'method', 'templated']
])
def test_upload_file_and_get_existent_fields(temp_folder, fields):
    link = f'{_TEST_DATA_URL}/test_txt.txt'
    file_path = f'{temp_folder}/fields_test{fields}.txt'
    response = helper.post_upload_resource_response(params=dict(path=file_path, url=link, fields=','.join(fields)))

    check.response_has_status_code(response, 202)
    check.response_has_only_fields(response, *fields)


def test_upload_file_by_unauthorized_user(temp_folder):
    link = f'{_TEST_DATA_URL}/test_txt.txt'
    file_path = f'{temp_folder}/unauthorized.txt'
    response = helper.post_upload_resource_response(params=dict(path=file_path, url=link), by_user='unauthorized')

    check.response_has_status_code(response, 401)
    check.response_does_not_have_fields(response, 'href')
    check.response_has_field_with_value(response, field='error', value='UnauthorizedError')


@pytest.mark.parametrize('path,url', [
    (None, None),
    (None, 'valid'),
    ('valid', None)
])
def test_upload_file_with_invalid_params(path, url, temp_folder):
    link = None if url is None else f'{_TEST_DATA_URL}/test_txt.txt'
    file_path = None if path is None else f'{temp_folder}/{url}{path}.txt'
    response = helper.post_upload_resource_response(params=dict(path=file_path, url=link))

    check.response_has_status_code(response, 400)
    check.response_does_not_have_fields(response, 'href')
    check.response_has_field_with_value(response, field='error', value='FieldValidationError')


def test_upload_file_with_empty_params():
    response = helper.post_upload_resource_response()

    check.response_has_status_code(response, 400)
    check.response_does_not_have_fields(response, 'href')
    check.response_has_field_with_value(response, field='error', value='FieldValidationError')
