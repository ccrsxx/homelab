import base64
import functools
from dataclasses import dataclass, field
from typing import Callable, ParamSpec, TypeVar
from urllib.parse import urljoin

import requests

from .env import app_env

Param = ParamSpec('Param')
ReType = TypeVar('ReType')


@dataclass
class Client:
    session: requests.Session = field(default_factory=requests.Session)
    session_authenticated: bool = False

    def login(self) -> None:
        print('Logging in to the router...')

        url = urljoin(app_env.ROUTER_URL, '/login.cgi')

        encrypted_password = base64.b64encode(app_env.ROUTER_PASSWORD.encode()).decode()

        hw_token = self.get_hardware_token()

        params = {
            'UserName': app_env.ROUTER_USERNAME,
            'PassWord': encrypted_password,
            'x.X_HW_Token': hw_token,
        }

        res = self.session.post(url, data=params)

        res.raise_for_status()

        self.session_authenticated = True

    def is_authenticated(
        self, func: Callable[Param, ReType]
    ) -> Callable[Param, ReType]:
        @functools.wraps(func)
        def wrapper(*args: Param.args, **kwargs: Param.kwargs) -> ReType:
            if not self.session_authenticated:
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
