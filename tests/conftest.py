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


@pytest.fixture(scope='session')
def temp_folder(base_folder):
    folders_paths = []

    def wrapped(path=base_folder):
        name = str(uuid.uuid4())
        folder_path = f'{path}/{name}'
        helper.put_resources(params={'path': folder_path})
        if path != base_folder:
            # storing folders with custom paths (base folder with all resources will be deleted anyway)
            folders_paths.append(folder_path)

        return folder_path, name

    yield wrapped

    for _path in folders_paths:
        helper.safe_delete(params={'path': _path})


@pytest.fixture(scope='session')
def temp_file(base_folder):
    files_paths = []

    def wrapped(path=base_folder):
        name = f'{uuid.uuid4()}.txt'
        file_path = f'{path}/{name}'
        link = config.data.TEST_DATA_URL['test_txt.txt']
        helper.upload_and_wait_status(params=dict(path=file_path, url=link), status='success')
        if path != base_folder:
            # storing files with custom paths (base folder with all resources will be deleted anyway)
            files_paths.append(file_path)

        return file_path, name

    yield wrapped

    for _path in files_paths:
        helper.safe_delete(params={'path': _path})
