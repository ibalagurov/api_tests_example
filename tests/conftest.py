import pytest
from testlib.resources import helper
import uuid


@pytest.fixture
def temp_folder():
    name = str(uuid.uuid4())
    helper.put_resources(params={'path': name})

    yield name

    helper.delete_resources(params={'path': name})
