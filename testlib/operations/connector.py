from requests import Request
import config

DISK_OPERATIONS_URL = config.routing.BASE_URL + '/disk/operations'


def disk_operations(operation_id, **kwargs):
    return Request(url=f'{DISK_OPERATIONS_URL}/{operation_id}', **kwargs)
