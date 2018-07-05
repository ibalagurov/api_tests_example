import allure
from functools import lru_cache
from requests import Session

import config


@lru_cache()
def get(by_user):
    if by_user not in ['authorized', 'unauthorized', 'expired']:
        raise ValueError(f'Undefined {by_user} user')
    session = Session()
    token = {'authorized': config.auth.TOKEN, 'expired': config.auth.EXPIRED_TOKEN}.get(by_user)
    if token:
        session.headers.update(Authorization=f'OAuth {token}')
    return session


def send_request(request, by_user):
    session = get(by_user=by_user)
    prepped = session.prepare_request(request)
    url, method, headers, body = prepped.url, prepped.method, prepped.headers, prepped.body
    request_info = f"send request:\n url: {url}\n method: {method}\n headers: {headers}\n body: {body}"
    allure.attach(request_info)
    if config.test_run.DEBUG:
        print(f'\n\n{request_info}')

    response = session.send(request=prepped, timeout=config.test_run.API_TIMEOUT, verify=config.routing.VERIFY_SSL)

    response_info = f"get response:\n code: {response.status_code} {response.reason}\n content: {response.text}"
    allure.attach(response_info)
    if config.test_run.DEBUG:
        print(request_info)

    return response
