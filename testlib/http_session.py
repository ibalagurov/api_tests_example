from functools import lru_cache
from requests import Session

import config


@lru_cache()
def get(by_user):
    session = Session()
    if by_user == 'authorized':
        session.headers.update(Authorization=f'OAuth {config.auth.TOKEN}')
    return session


def send_request(request, by_user):
    session = get(by_user=by_user)
    prepped = session.prepare_request(request)
    if config.test_run.DEBUG:
        print(f"""
            send request:
                url: {prepped.url}
                method: {prepped.method}
                headers: {prepped.headers}
                body: {prepped.body}""")

    response = session.send(request=prepped, timeout=config.test_run.API_TIMEOUT, verify=config.routing.VERIFY_SSL)

    if config.test_run.DEBUG:
        print(f"""
            get response:
                code: {response.status_code} {response.reason}
                content: {response.text}""")

    return response
