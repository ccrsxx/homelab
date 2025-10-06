import base64
import functools
from typing import Any, Callable, ParamSpec, TypeVar
from urllib.parse import urljoin

import requests

from .config import app_config
from .env import app_env

Param = ParamSpec('Param')
ReType = TypeVar('ReType')


class TimeoutHTTPAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if 'timeout' in kwargs:
            self.timeout = kwargs['timeout']
            del kwargs['timeout']

        super().__init__(*args, **kwargs)

    def send(  # type: ignore
        self,
        request: requests.models.PreparedRequest,
        **kwargs: Any,
    ) -> requests.models.Response:
        timeout = kwargs.get('timeout')

        if timeout is None and hasattr(self, 'timeout'):
            kwargs['timeout'] = self.timeout

        return super().send(request, **kwargs)


class Client:
    def __init__(self) -> None:
        self.session = requests.Session()

        timeout_adapter = TimeoutHTTPAdapter(timeout=app_config['REQUEST_TIMEOUT'])

        self.session.mount('http://', timeout_adapter)
        self.session.mount('https://', timeout_adapter)

    def login(self) -> None:
        LOGIN_RETRIES = 3

        for attempt in range(1, LOGIN_RETRIES + 1):
            try:
                print('Logging in to the router...')

                url = urljoin(app_env.ROUTER_URL, '/login.cgi')

                encrypted_password = base64.b64encode(
                    app_env.ROUTER_PASSWORD.encode()
                ).decode()

                hw_token = self.get_hardware_token()

                params = {
                    'UserName': app_env.ROUTER_USERNAME,
                    'PassWord': encrypted_password,
                    'x.X_HW_Token': hw_token,
                }

                res = self.session.post(url, data=params)

                res.raise_for_status()

                break
            except Exception as e:
                print(f'Login attempt {attempt } failed: {e}')

                if attempt == LOGIN_RETRIES:
                    print('All login attempts failed.')
                else:
                    print('Retrying...')

        is_authenticated = self.check_is_authenticated()

        if not is_authenticated:
            raise Exception('Failed to authenticate with the router.')

    def check_is_authenticated(self) -> bool:
        url = urljoin(app_env.ROUTER_URL, '/html/ssmp/common/refreshTime.asp')

        response = self.session.get(url)

        try:
            response.raise_for_status()

            parsed_text_response = response.text.strip()

            is_logged_in = parsed_text_response == '1'

            return is_logged_in
        except Exception as e:
            print('Error checking authentication status:', e)
            return False

    def is_authenticated(
        self, func: Callable[Param, ReType]
    ) -> Callable[Param, ReType]:
        @functools.wraps(func)
        def wrapper(*args: Param.args, **kwargs: Param.kwargs) -> ReType:
            is_currently_authenticated = self.check_is_authenticated()

            print(f'Currently authenticated: {is_currently_authenticated}')

            if not is_currently_authenticated:
                self.login()

            return func(*args, **kwargs)

        return wrapper

    def get_hardware_token(self) -> str:
        url = urljoin(app_env.ROUTER_URL, '/asp/GetRandCount.asp')

        res = self.session.post(url)

        res.raise_for_status()

        raw_token = res.text.strip()

        parsed_token = raw_token[-48:]

        return parsed_token
