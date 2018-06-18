from requests import Request
from functools import partial

import config

DISK_URL = config.routing.BASE_URL + '/disk'

disk = partial(Request, url=DISK_URL)
