import pytest
import allure
from testlib import check
from testlib import helper as helper


@allure.story("Authorized user can get disk information")
def test_get_disk_info():
    response = helper.get_disk_info_response()
    check.response_has_status_code(response, 200)
    check.response_has_fields(response, 'system_folders', 'user', 'max_file_size', 'is_paid', 'used_space')


def test_unauthorized_user_do_not_have_access_to_disk_info():
    response = helper.get_disk_info_response(by_user='unauthorized')
    check.response_has_status_code(response, 401)
    check.response_has_field_with_value(response, field='error', value='UnauthorizedError')
    check.response_does_not_have_fields(
        response, 'system_folders', 'user', 'max_file_size', 'is_paid', 'used_space'
    )


def test_expired_user_do_not_have_access_to_disk_info():
    response = helper.get_disk_info_response(by_user='expired')
    check.response_has_status_code(response, 401)
    check.response_has_field_with_value(response, field='error', value='UnauthorizedError')
    check.response_does_not_have_fields(
        response, 'system_folders', 'user', 'max_file_size', 'is_paid', 'used_space'
    )


@pytest.mark.parametrize('method', ['post', 'put', 'delete', 'patch'])
def test_unexpected_methods_are_not_allowed(method):
    response = helper.custom_disk_response(method=method, by_user='authorized')
    check.response_has_status_code(response, 405)
    check.response_has_field_with_value(response, field='error', value='MethodNotAllowedError')
