from testlib import disk


def test_disk_info():
    response = disk.helper.get_disk_info_response()
    assert response.status_code == 200
    j = response.json()
    assert j
