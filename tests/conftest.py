import pytest
import uuid

import config
from testlib import helper


@pytest.fixture(scope='session')
def base_folder():
    """ Temp folder is created once before test run, and will be deleted after """
    name = str(uuid.uuid4())
    helper.put_resources(params={'path': name})

    yield name

    helper.delete_resources(params={'path': name})


@pytest.fixture(scope='function')
def temp_folder():
    folders_paths = []

    def wrapped(path=''):
        name = str(uuid.uuid4())
        folder_path = f'{path}/{name}'
        helper.put_resources(params={'path': folder_path})
        folders_paths.append(folder_path)

        return name

    yield wrapped

    for _path in folders_paths:
        helper.delete_resources(params={'path': _path})


@pytest.fixture(scope='function')
def temp_file():
    files_paths = []

    def wrapped(path=''):
        name = f'{uuid.uuid4()}.txt'
        file_path = f'{path}/{name}'
        link = f'{config.data.TEST_DATA_URL}/test_txt.txt'
        helper.upload_and_wait_status(params=dict(path=file_path, url=link), status='success')
        files_paths.append(file_path)

        return name

    yield wrapped

    for _path in files_paths:
        helper.delete_resources(params={'path': _path})
