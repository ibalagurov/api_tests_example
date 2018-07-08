import pytest
import allure
from testlib import http_session
from testlib import helper
from testlib import check


@pytest.fixture(scope='module')
@allure.step("There is file")
def module_file(temp_file):
    path, file_name = temp_file()
    return path, file_name


@pytest.fixture(scope='module')
@allure.step("There is folder")
def module_folder(temp_folder):
    path, folder_name = temp_folder()
    return path, folder_name


@allure.feature("Publishing resource")
@allure.story("Authorized user can publish file")
@allure.severity(allure.severity_level.BLOCKER)
def test_publish_file(module_file):
    file_path, file_name, *_ = module_file

    response = helper.put_publish_resource_response(params=dict(path=file_path))

    check.response_has_status_code(response, 200)
    check.response_has_only_fields(response, 'href', 'method', 'templated')
    check.response_has_field_contains_value(response, 'href', file_name)

    with allure.step("There is should be only one copy of published file"):
        items = helper.get_public_resources().get('items')
        items_by_name = [item for item in items if item.get('name') == file_name]
        assert len(items_by_name) == 1, "There is should be only one copy of published file"

    with allure.step("Published file should be available even for unauthorized user"):
        response = http_session.send_custom_request(method='get', by_user='unauthorized', url=items_by_name[0]['file'])
        check.response_has_status_code(response, 200)


@allure.feature("Publishing resource")
@allure.story("Authorized user can publish folder")
@allure.severity(allure.severity_level.BLOCKER)
def test_publish_folder(module_folder):
    folder_path, folder_name, *_ = module_folder

    response = helper.put_publish_resource_response(params=dict(path=folder_path))

    check.response_has_status_code(response, 200)
    check.response_has_only_fields(response, 'href', 'method', 'templated')
    check.response_has_field_contains_value(response, 'href', folder_name)

    with allure.step("There is should be only one copy of published folder"):
        items = helper.get_public_resources().get('items')
        items_by_name = [item for item in items if item.get('name') == folder_name]
        assert len(items_by_name) == 1, "There is should be only one copy of published folder"

    with allure.step("Published folder should be available even for unauthorized user"):
        response = http_session.send_custom_request(
            method='get', by_user='unauthorized', url=items_by_name[0]['public_url']
        )
        check.response_has_status_code(response, 200)


@allure.feature("Publishing resource")
@allure.story("Unauthorized user should not be able to publish a file")
@allure.severity(allure.severity_level.BLOCKER)
def test_publish_file_by_unauthorized_user(module_file):
    file_path, file_name, *_ = module_file

    response = helper.put_publish_resource_response(params=dict(path=file_path), by_user='unauthorized')

    check.response_has_status_code(response, 401)
    check.response_has_only_fields(response, 'message', 'description', 'error')
    check.response_has_field_with_value(response, field='error', value='UnauthorizedError')


@allure.feature("Publishing resource")
@allure.story("User with expired token should not be able to publish a folder")
@allure.severity(allure.severity_level.BLOCKER)
def test_publish_folder_by_expired_user(module_folder):
    folder_path, folder_name, *_ = module_folder

    response = helper.put_publish_resource_response(params=dict(path=folder_path), by_user='expired')

    check.response_has_status_code(response, 401)
    check.response_has_only_fields(response, 'message', 'description', 'error')
    check.response_has_field_with_value(response, field='error', value='UnauthorizedError')


@allure.feature("Publishing resource")
@allure.story("User should get not found error on publishing nonexistent file")
@allure.severity(allure.severity_level.NORMAL)
def test_publish_nonexistent_file():
    response = helper.put_publish_resource_response(params=dict(path='nonexistent_file'))

    check.response_has_status_code(response, 404)
    check.response_has_only_fields(response, 'message', 'description', 'error')
    check.response_has_field_with_value(response, field='error', value='DiskNotFoundError')


@allure.feature("Publishing resource")
@allure.story("Filtering fields during publishing a resource")
@allure.severity(allure.severity_level.MINOR)
def test_publish_and_filter_fields(module_folder):
    folder_path, folder_name, *_ = module_folder

    response = helper.put_publish_resource_response(params=dict(path=folder_path, fields='href,method'))

    check.response_has_status_code(response, 200)
    check.response_has_only_fields(response, 'href', 'method')
