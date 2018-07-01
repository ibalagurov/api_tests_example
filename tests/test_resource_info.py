import pytest
from testlib import helper
from testlib import check


@pytest.fixture(scope='module')
def folder_with_two_files(temp_folder, temp_file):
    folder_path, *_ = temp_folder()
    file, *_ = temp_file(path=folder_path)
    file_2, *_ = temp_file(path=folder_path)
    return folder_path, file, file_2


@pytest.fixture(scope='module')
def module_file(temp_file):
    path, file_name = temp_file()
    return path, file_name


@pytest.fixture(scope='module')
def module_folder(temp_folder):
    path, folder_name = temp_folder()
    return path, folder_name


def test_meta_for_file(module_file):
    path, file_name = module_file

    response = helper.get_resources_response(params=dict(path=path))

    check.response_has_status_code(response, 200)
    check.response_has_fields(
        response,
        'antivirus_status', 'file', 'sha256', 'name', 'exif', 'created', 'resource_id', 'modified', 'path',
        'comment_ids', 'type', 'revision', 'media_type', 'md5', 'mime_type', 'size'
    )
    check.response_has_field_with_value(response, "type", 'file')
    check.response_has_field_with_value(response, "mime_type", 'text/plain')
    check.response_has_field_with_value(response, "name", file_name)


def test_meta_for_folder(module_folder):
    path, folder_name = module_folder

    response = helper.get_resources_response(params=dict(path=path))

    check.response_has_status_code(response, 200)
    check.response_has_only_fields(
        response,
        '_embedded', 'name', 'exif', 'created', 'resource_id', 'modified', 'path', 'comment_ids', 'type', 'revision'
    )
    check.response_has_field_with_value(response, "type", 'dir')
    check.response_has_field_with_value(response, "name", folder_name)


def test_filter_fields_for_file(module_file):
    file, *_ = module_file

    response = helper.get_resources_response(params=dict(path=file, fields='size'))

    check.response_has_status_code(response, 200)
    check.response_has_only_fields(response, 'size')


def test_filter_fields_for_folder(module_folder):
    folder, *_ = module_folder

    response = helper.get_resources_response(params=dict(path=folder, fields='_embedded'))

    check.response_has_status_code(response, 200)
    check.response_has_only_fields(response, '_embedded')


@pytest.mark.parametrize('limit,expected_items,expected_limit', [
                            (None, 2, 20),  # 20 - default limit
                            (0, 0, 0),
                            (1, 1, 1),
                            (-1, 1, -1),  # unclear usage
                            (2, 2, 2),
                            (3, 2, 3)
])
def test_limit_nested_resources(folder_with_two_files, limit, expected_items, expected_limit):
    folder, *_ = folder_with_two_files

    response = helper.get_resources_response(params=dict(path=folder, limit=limit))

    check.response_has_status_code(response, 200)
    check.response_has_fields(response, '_embedded')
    json = response.json()
    embedded = json['_embedded']
    assert len(embedded.get('items')) == expected_items
    assert embedded.get('limit') == expected_limit


@pytest.mark.parametrize('sorting_type', ['created', 'name', 'modified'])
def test_sort_resources(folder_with_two_files, sorting_type):
    folder, *_ = folder_with_two_files

    response = helper.get_resources_response(params=dict(path=folder, sort=sorting_type))

    check.response_has_status_code(response, 200)
    check.response_has_fields(response, '_embedded')
    json = response.json()
    embedded = json['_embedded']
    items = embedded['items']
    expected_items = sorted(items, key=lambda item: item[sorting_type])
    assert items == expected_items


def test_offset_nested_resources(folder_with_two_files):
    folder, file_1, file_2, *_ = folder_with_two_files

    response = helper.get_resources_response(params=dict(path=folder, offset=1, sort='created'))

    check.response_has_status_code(response, 200)
    check.response_has_fields(response, '_embedded')
    json = response.json()
    embedded = json['_embedded']
    items = embedded.get('items')
    assert len(items) == 1, "Should be only one file (2 files in directory and offset is 1)"

    item = items[0]
    assert file_2 in item['path'], "Files should be sorted by created date (default sorting type)"


def test_unauthorized_user(module_folder):
    folder, *_ = module_folder

    response = helper.get_resources_response(params=dict(path=folder), by_user='unauthorized')

    check.response_has_status_code(response, 401)
    check.response_has_only_fields(response, 'message', 'description', 'error')
    check.response_has_field_with_value(response, field='error', value='UnauthorizedError')


def test_expired_user(module_folder):
    folder, *_ = module_folder

    response = helper.get_resources_response(params=dict(path=folder), by_user='expired')

    check.response_has_status_code(response, 401)
    check.response_has_only_fields(response, 'message', 'description', 'error')
    check.response_has_field_with_value(response, field='error', value='UnauthorizedError')


@pytest.mark.parametrize('limit,offset', [
    (None, 'asd'),
    ('qwe', None),
    ('1a', '2c')
])
def test_bad_request(module_folder, limit, offset):
    folder, *_ = module_folder

    response = helper.get_resources_response(params=dict(path=folder, limit=limit, offset=offset))

    check.response_has_status_code(response, 400)
    check.response_has_only_fields(response, 'message', 'description', 'error')
    check.response_has_field_with_value(response, field='error', value='FieldValidationError')


def test_not_found(base_folder):
    response = helper.get_resources_response(params=dict(path=f'{base_folder}/nonexistent.txt'))

    check.response_has_status_code(response, 404)
    check.response_has_only_fields(response, 'message', 'description', 'error')
    check.response_has_field_with_value(response, field='error', value='DiskNotFoundError')
