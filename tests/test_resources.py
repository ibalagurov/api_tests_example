import pytest
from testlib import helper
from testlib import check
from waiting import wait


_TEST_DATA_URL = 'https://github.com/ibalagurov/api_tests_example/blob/master/test_data'


@pytest.mark.parametrize('file_name, link, mime_type', [
    ('test.jpg', f'{_TEST_DATA_URL}/test_jpg.jpg', 'image/jpeg'),
    ('test.json', f'{_TEST_DATA_URL}/test_json.json', 'application/octet-stream'),
    ('test.txt', f'{_TEST_DATA_URL}/test_txt.txt', 'text/plain'),
])
def test_upload(temp_folder, file_name, link, mime_type):
    """ Temporary folder is created, upload in it image, operation should be successful, file should be available and
        have expected name and mime type """
    file_path = f'{temp_folder}/{file_name}'
    response = helper.post_upload_resource_response(params={'path': file_path, 'url': link})

    check.response_has_status_code(response, 202)
    check.response_has_fields(response, 'href')
    href = response.json().get('href')
    operation_id = href.split('/')[-1]

    wait(predicate=lambda: helper.operation_status(operation_id=operation_id) == 'success')

    response = helper.get_resources_response(params={'path': file_path})
    check.response_has_status_code(response, 200)
    check.response_has_field_with_value(response, "mime_type", mime_type)
    check.response_has_field_with_value(response, "name", file_name)
