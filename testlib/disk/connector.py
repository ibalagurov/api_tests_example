from requests import Request

import config

DISK_URL = config.routing.BASE_URL + '/disk'


def disk(method):
    return Request(method=method, url=DISK_URL)
