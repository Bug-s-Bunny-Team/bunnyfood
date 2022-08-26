from functools import partial

import requests.utils

from instaloader import Instaloader, InstaloaderContext


class ContextProxy:
    def __init__(self, context: InstaloaderContext):
        self._context = context

    def __getattr__(self, attr):
        return getattr(self._context, attr)

    def export_session_as_dict(self) -> dict:
        return requests.utils.dict_from_cookiejar(self._context._session.cookies)

    def import_session_from_dict(self, session_dict: dict, username: str):
        session = requests.Session()
        session.cookies = requests.utils.cookiejar_from_dict(session_dict)
        session.headers.update(self._default_http_header())
        session.headers.update({'X-CSRFToken': session.cookies.get_dict()['csrftoken']})
        session.request = partial(session.request, timeout=self._context.request_timeout)  # type: ignore
        self._context._session = session
        self._context.username = username


class CustomInstaloader(Instaloader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = ContextProxy(self.context)

    def export_session_as_dict(self) -> dict:
        return self.context.export_session_as_dict()

    def import_session_from_dict(self, session_dict: dict, username: str):
        self.context.import_session_from_dict(session_dict, username)
