from testlib import helper
from testlib import check


def test_meta_for_file(base_folder, temp_file):
    """ Temporary folder is created, upload in it image, operation should be successful, file should be available and
        have expected name and mime type """
    file_name = temp_file(path=base_folder)

    response = helper.get_resources_response(params=dict(path=f'{base_folder}/{file_name}'))
    check.response_has_status_code(response, 200)
    check.response_has_field_with_value(response, "mime_type", 'text/plain')
    check.response_has_field_with_value(response, "name", file_name)
