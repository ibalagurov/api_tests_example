import pytest
import allure
from waiting import wait
from testlib import helper
from testlib import check


@pytest.fixture
@allure.step("There are folder with two files inside")
def folder_with_file(temp_folder, temp_file):
    folder_path, folder_name, *_ = temp_folder()
    file, *_ = temp_file(path=folder_path)
    return folder_path, folder_name, file


@pytest.fixture
@allure.step("There is published folder")
def published_folder(temp_folder):
    path, folder_name = temp_folder()
    helper.put_publish_resource(params=dict(path=path))
    return path, folder_name


@pytest.fixture
@allure.step("There is published file")
def published_file(temp_file):
    path, file_name = temp_file()
    helper.put_publish_resource(params=dict(path=path))
    return path, file_name


@allure.feature("Deleting resource")
@allure.story("Authorized user can delete a file")
@allure.severity(allure.severity_level.BLOCKER)
def test_delete_file(temp_file):
    path, file_name, *_ = temp_file()

    response = helper.delete_resources_response(params=dict(path=path))

    check.response_has_status_code(response, 202, 204)

    with allure.step("Waiting when file will be deleted"):
        wait(
            predicate=lambda: helper.get_resources_response(params=dict(path=path)).status_code == 404,
            timeout_seconds=30, sleep_seconds=(1, 2, 4)
        )

    with allure.step("Deleted file should be in trash folder"):
        file_in_trash = helper.get_trash_resources(params=dict(path=file_name))
        assert file_in_trash['name'] == file_name, 'Unable to find deleted file in trash'


@allure.feature("Deleting resource")
@allure.story("Authorized user can delete a folder")
@allure.severity(allure.severity_level.BLOCKER)
def test_delete_folder(temp_folder):
    path, folder_name, *_ = temp_folder()

    response = helper.delete_resources_response(params=dict(path=path))

    check.response_has_status_code(response, 202, 204)

    with allure.step("Waiting when folder will be deleted"):
        wait(
            predicate=lambda: helper.get_resources_response(params=dict(path=path)).status_code == 404,
            timeout_seconds=30, sleep_seconds=(1, 2, 4)
        )

    with allure.step("Deleted folder should be in trash folder"):
        folder_in_trash = helper.get_trash_resources(params=dict(path=folder_name))
        assert folder_in_trash['name'] == folder_name, 'Unable to find deleted folder in trash'


@allure.feature("Deleting resource")
@allure.story("Authorized user can delete a folder with files inside")
@allure.severity(allure.severity_level.CRITICAL)
def test_delete_folder_with_files(folder_with_file):
    path, folder_name, *_ = folder_with_file

    response = helper.delete_resources_response(params=dict(path=path))

    check.response_has_status_code(response, 202, 204)

    with allure.step("Waiting when folder will be deleted"):
        wait(
            predicate=lambda: helper.get_resources_response(params=dict(path=path)).status_code == 404,
            timeout_seconds=30, sleep_seconds=(1, 2, 4)
        )

    with allure.step("Deleted folder should be in trash folder"):
        file_in_trash = helper.get_trash_resources(params=dict(path=folder_name))
        assert file_in_trash['name'] == folder_name, 'Unable to find deleted folder in trash'


@allure.feature("Deleting resource")
@allure.story("Authorized user can delete a published file")
@allure.severity(allure.severity_level.CRITICAL)
def test_delete_published_file(published_file):
    path, file_name, *_ = published_file

    response = helper.delete_resources_response(params=dict(path=path))
    check.response_has_status_code(response, 202, 204)

    with allure.step("Waiting when file will be deleted"):
        wait(
            predicate=lambda: helper.get_resources_response(params=dict(path=path)).status_code == 404,
            timeout_seconds=30, sleep_seconds=(1, 2, 4)
        )

    with allure.step("Deleted folder should be in trash folder"):
        file_in_trash = helper.get_trash_resources(params=dict(path=file_name))
        assert file_in_trash['name'] == file_name, 'Unable to find deleted file in trash'

    with allure.step("Deleted file should be unpublished"):
        items = helper.get_public_resources().get('items')
        items_by_name = [item for item in items if item.get('name') == file_name]
        assert len(items_by_name) == 0, "Deleted file still published"


@allure.feature("Deleting resource")
@allure.story("Authorized user can delete a published folder")
@allure.severity(allure.severity_level.CRITICAL)
def test_delete_published_folder(published_folder):
    path, folder_name, *_ = published_folder

    response = helper.delete_resources_response(params=dict(path=path))

    check.response_has_status_code(response, 202, 204)

    with allure.step("Waiting when folder will be deleted"):
        wait(
            predicate=lambda: helper.get_resources_response(params=dict(path=path)).status_code == 404,
            timeout_seconds=30, sleep_seconds=(1, 2, 4)
        )

    with allure.step("Deleted folder should be in trash folder"):
        folder_in_trash = helper.get_trash_resources(params=dict(path=folder_name))
        assert folder_in_trash['name'] == folder_name, 'Unable to find deleted folder in trash'

    with allure.step("Deleted folder should be unpublished"):
        items = helper.get_public_resources().get('items')
        items_by_name = [item for item in items if item.get('name') == folder_name]
        assert len(items_by_name) == 0, "Deleted file still published"


@allure.feature("Deleting resource")
@allure.story("The deletion operation can be forced asynchronously")
@allure.severity(allure.severity_level.MINOR)
def test_delete_folder_force_async(temp_folder):
    path, folder_name, *_ = temp_folder()

    response = helper.delete_resources_response(params=dict(path=path, force_async=True))
    check.response_has_status_code(response, 202)

    operation_id = helper.get_operation_id_from_response(response)
    helper.when_operation_status(operation_id=operation_id, status='success')

    with allure.step("Deleted folder should be in trash folder"):
        file_in_trash = helper.get_trash_resources(params=dict(path=folder_name))
        assert file_in_trash['name'] == folder_name, 'Unable to find deleted folder in trash'


@allure.feature("Deleting resource")
@allure.story("User can delete file permanently")
@allure.severity(allure.severity_level.NORMAL)
def test_delete_file_permanently(temp_file):
    path, file_name, *_ = temp_file()

    response = helper.delete_resources_response(params=dict(path=path, permanently=True))
    check.response_has_status_code(response, 202, 204)

    with allure.step("Waiting when file will be deleted"):
        wait(
            predicate=lambda: helper.get_resources_response(params=dict(path=path)).status_code == 404,
            timeout_seconds=30, sleep_seconds=(1, 2, 4)
        )

    with allure.step("Deleted permanently file should not be in trash folder"):
        response = helper.get_trash_resources_response(params=dict(path=file_name))
        assert response.status_code == 404, 'Deleted permanently file should not be in trash'


@allure.feature("Deleting resource")
@allure.story("User should get not found error on deleting nonexistent resource")
@allure.severity(allure.severity_level.NORMAL)
def test_delete_nonexistent_resource():
    response = helper.delete_resources_response(params=dict(path='nonexistent.txt'))

    check.response_has_status_code(response, 404)
    check.response_has_only_fields(response, 'message', 'description', 'error')
    check.response_has_field_with_value(response, field='error', value='DiskNotFoundError')


@allure.feature("Deleting resource")
@allure.story("Unauthorized user should not be able to delete a folder")
@allure.severity(allure.severity_level.BLOCKER)
def test_delete_folder_by_unauthorized_user(temp_folder):
    path, *_ = temp_folder()

    response = helper.delete_resources_response(params=dict(path=path), by_user='unauthorized')

    check.response_has_status_code(response, 401)
    check.response_has_only_fields(response, 'message', 'description', 'error')
    check.response_has_field_with_value(response, field='error', value='UnauthorizedError')


@allure.feature("Deleting resource")
@allure.story("Unauthorized user should not be able to delete a file")
@allure.severity(allure.severity_level.BLOCKER)
def test_delete_file_by_expired_user(temp_file):
    path, *_ = temp_file()

    response = helper.delete_resources_response(params=dict(path=path), by_user='expired')

    check.response_has_status_code(response, 401)
    check.response_has_only_fields(response, 'message', 'description', 'error')
    check.response_has_field_with_value(response, field='error', value='UnauthorizedError')
