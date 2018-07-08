import pytest
import allure
import config
from testlib import helper
from testlib import check


@allure.feature("Uploading file from url")
@allure.story("Authorized user can upload files")
@allure.severity(allure.severity_level.BLOCKER)
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

    with allure.step("File information should be available"):
        response = helper.get_resources_response(params=dict(path=file_path))
        check.response_has_status_code(response, 200)
        check.response_has_field_with_value(response, "mime_type", mime_type)
        check.response_has_field_with_value(response, "name", file_name)


@allure.feature("Uploading file from url")
@allure.story("For files with same names should be added postfix")
@allure.severity(allure.severity_level.CRITICAL)
def test_uploaded_file_with_same_name_should_have_postfix(base_folder):
    file_path = f'{base_folder}/same_name.txt'
    link = config.data.TEST_DATA_URL['test_txt.txt']
    helper.upload_and_wait_status(params=dict(path=file_path, url=link), status='success')
    helper.upload_and_wait_status(params=dict(path=file_path, url=link), status='success')

    with allure.step("First file was uploaded with original name"):
        response = helper.get_resources_response(params=dict(path=file_path))
        check.response_has_status_code(response, 200)
        check.response_has_field_with_value(response, "name", 'same_name.txt')

    with allure.step("Second file was uploaded with postfix"):
        response = helper.get_resources_response(params=dict(path=f'{base_folder}/same_name (1).txt'))
        check.response_has_status_code(response, 200)
        check.response_has_field_with_value(response, "name", 'same_name (1).txt')


@allure.feature("Uploading file from url")
@allure.story("Used space should be increased after file was uploaded")
@allure.severity(allure.severity_level.BLOCKER)
def test_file_uploading_should_increase_used_space(base_folder):
    file_path = f'{base_folder}/used_space.txt'
    link = config.data.TEST_DATA_URL['test_txt.txt']

    space_before = helper.get_disk_info().get('used_space')

    helper.upload_and_wait_status(params=dict(path=file_path, url=link), status='success')

    with allure.step("Used space was increased"):
        space_after = helper.get_disk_info().get('used_space')
        assert space_after > space_before, "Used space wasn't changed after file uploading"


@allure.feature("Uploading file from url")
@allure.story("User should get expected error for trying upload file to nonexistent folder")
@allure.severity(allure.severity_level.NORMAL)
def test_upload_file_to_nonexistent_folder():
    link = config.data.TEST_DATA_URL['test_txt.txt']
    file_path = f'nonexistent_folder/existed_file.txt'
    response = helper.post_upload_resource_response(params=dict(path=file_path, url=link))

    check.response_has_status_code(response, 409)
    check.response_has_only_fields(response, 'message', 'description', 'error')
    check.response_has_field_with_value(response, field='error', value='DiskPathDoesntExistsError')


@allure.feature("Uploading file from url")
@allure.story("Upload from nonexistent url should be failed")
@allure.severity(allure.severity_level.MINOR)
def test_upload_file_from_nonexistent_url(base_folder):
    link = config.data.TEST_DATA_URL['nonexistent_url']
    file_path = f'{base_folder}/from_nonexistent_url.txt'

    helper.upload_and_wait_status(params=dict(path=file_path, url=link), status='failed')


@allure.feature("Uploading file from url")
@allure.story("Filtering fields during upload")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.parametrize('fields', [
    ['href'], ['href', 'method'], ['href', 'method', 'templated']
])
def test_upload_file_and_get_existent_fields(base_folder, fields):
    link = config.data.TEST_DATA_URL['test_txt.txt']
    file_path = f'{base_folder}/fields_test{fields}.txt'
    response = helper.post_upload_resource_response(params=dict(path=file_path, url=link, fields=','.join(fields)))

    check.response_has_status_code(response, 202)
    check.response_has_only_fields(response, *fields)


@allure.feature("Uploading file from url")
@allure.story("Unauthorized user should not be able to upload files")
@allure.severity(allure.severity_level.BLOCKER)
def test_upload_file_by_unauthorized_user(base_folder):
    link = config.data.TEST_DATA_URL['test_txt.txt']
    file_path = f'{base_folder}/unauthorized.txt'
    response = helper.post_upload_resource_response(params=dict(path=file_path, url=link), by_user='unauthorized')

    check.response_has_status_code(response, 401)
    check.response_has_only_fields(response, 'message', 'description', 'error')
    check.response_has_field_with_value(response, field='error', value='UnauthorizedError')


@allure.feature("Uploading file from url")
@allure.story("User with expired token should not be able to upload files")
@allure.severity(allure.severity_level.BLOCKER)
def test_upload_file_by_unauthorized_user(base_folder):
    link = config.data.TEST_DATA_URL['test_txt.txt']
    file_path = f'{base_folder}/unauthorized.txt'
    response = helper.post_upload_resource_response(params=dict(path=file_path, url=link), by_user='expired')

    check.response_has_status_code(response, 401)
    check.response_has_only_fields(response, 'message', 'description', 'error')
    check.response_has_field_with_value(response, field='error', value='UnauthorizedError')


@allure.feature("Uploading file from url")
@allure.story("Unauthorized user should not be able to upload files")
@allure.severity(allure.severity_level.BLOCKER)
def test_upload_file_by_unauthorized_user(base_folder):
    link = config.data.TEST_DATA_URL['test_txt.txt']
    file_path = f'{base_folder}/unauthorized.txt'
    response = helper.post_upload_resource_response(params=dict(path=file_path, url=link), by_user='unauthorized')

    check.response_has_status_code(response, 401)
    check.response_has_only_fields(response, 'message', 'description', 'error')
    check.response_has_field_with_value(response, field='error', value='UnauthorizedError')


@allure.feature("Uploading file from url")
@allure.story("Non-valid path or/and url should get expected error")
@allure.severity(allure.severity_level.MINOR)
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


@allure.feature("Uploading file from url")
@allure.story("Non-valid path or/and url should get expected error")
@allure.severity(allure.severity_level.MINOR)
def test_upload_file_with_empty_params():
    response = helper.post_upload_resource_response()

    check.response_has_status_code(response, 400)
    check.response_has_only_fields(response, 'message', 'description', 'error')
    check.response_has_field_with_value(response, field='error', value='FieldValidationError')
