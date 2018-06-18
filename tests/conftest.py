import pytest
from testlib.resources import helper
import uuid


@pytest.fixture(scope='session')
def temp_folder():
    """ Temp folder is created once before test run, and will be deleted after """
    name = str(uuid.uuid4())
    helper.put_resources(params={'path': name})

    yield name

    helper.delete_resources(params={'path': name})
