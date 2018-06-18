from testlib import resources, operations
from waiting import wait


def test_upload(temp_folder):
    test_link = 'https://habrastorage.org/getpro/habr/post_images/ac4/d9f/2a9/ac4d9f2a99bca3d3342b7f440f62ba3d.jpg'
    file_path = f'{temp_folder}/test.jpg'
    response = resources.helper.post_upload_resource_response(
        params={'path': file_path, 'url': test_link}
    )
    assert response.status_code == 202
    href = response.json().get('href')
    assert href
    operation_id = href.split('/')[-1]
    wait(predicate=lambda: operations.helper.get_operations_status(operation_id=operation_id) == 'success')
    response = resources.helper.get_resources_response(
        params={'path': file_path}
    )
    assert response.status_code == 200
