from requests import Request
from functools import partial
import config

DISK_RESOURCES_URL = config.routing.BASE_URL + '/disk/resources'
DISK_RESOURCE_UPLOAD_URL = DISK_RESOURCES_URL + '/upload'
DISK_RESOURCE_PUBLISH_URL = DISK_RESOURCES_URL + '/publish'

disk_resources = partial(Request, url=DISK_RESOURCES_URL)
disk_resource_publish = partial(Request, url=DISK_RESOURCE_PUBLISH_URL)
disk_resource_upload = partial(Request, url=DISK_RESOURCE_UPLOAD_URL)
