from testlib import resources, operations
from testlib import check
from waiting import wait


def test_upload(temp_folder):
    """ Temporary folder is created, upload in it image, operation should be successful, file should be available and
        have expected name and mime type """
    test_link = 'https://habrastorage.org/getpro/habr/post_images/ac4/d9f/2a9/ac4d9f2a99bca3d3342b7f440f62ba3d.jpg'
    file_path = f'{temp_folder}/test.jpg'
    response = resources.helper.post_upload_resource_response(params={'path': file_path, 'url': test_link})

    check.response_has_status_code(response, 202)
    check.response_has_fields(response, 'href')
    href = response.json().get('href')
    operation_id = href.split('/')[-1]

    wait(predicate=lambda: operations.helper.get_operations_status(operation_id=operation_id) == 'success')

    response = resources.helper.get_resources_response(params={'path': file_path})
    check.response_has_status_code(response, 200)
    check.response_has_field_with_value(response, "type", "file")
    check.response_has_field_with_value(response, "mime_type", "image/jpeg")
    check.response_has_field_with_value(response, "name", "test.jpg")
