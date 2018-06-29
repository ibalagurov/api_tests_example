from testlib import helper
from testlib import check


def test_meta_for_file(base_folder, temp_file):
    file_name = temp_file(path=base_folder)

    response = helper.get_resources_response(params=dict(path=f'{base_folder}/{file_name}'))

    check.response_has_status_code(response, 200)
    check.response_has_only_fields(
        response,
        'antivirus_status', 'file', 'sha256', 'name', 'exif', 'created', 'resource_id', 'modified', 'path',
        'comment_ids', 'type', 'revision', 'media_type', 'md5', 'mime_type', 'size'
    )
    check.response_has_field_with_value(response, "type", 'file')
    check.response_has_field_with_value(response, "mime_type", 'text/plain')
    check.response_has_field_with_value(response, "name", file_name)


def test_meta_for_folder(base_folder, temp_folder):
    folder_name = temp_folder(path=base_folder)

    response = helper.get_resources_response(params=dict(path=f'{base_folder}/{folder_name}'))

    check.response_has_status_code(response, 200)
    check.response_has_only_fields(
        response,
        '_embedded', 'name', 'exif', 'created', 'resource_id', 'modified', 'path', 'comment_ids', 'type', 'revision'
    )
    check.response_has_field_with_value(response, "type", 'dir')
    check.response_has_field_with_value(response, "name", folder_name)


def test_filter_fields_for_file():
    pass


def test_filter_fields_for_folder():
    pass


def test_limit_nested_resources():
    pass


def test_offset_nested_resources():
    pass


def test_unauthorized_user():
    pass


def test_non_valid_user():
    pass


def test_bad_request():
    pass


def test_not_found():
    pass
