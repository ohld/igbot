import json
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

import requests
import responses

from instabot import Bot
from instabot.api.config import API_URL

DEFAULT_RESPONSE = {'status': 'ok'}


class TestBot:
    def setup(self):
        self.USER_ID = 1234567
        self.USERNAME = 'test_username'
        self.PASSWORD = 'test_password'
        self.FULLNAME = 'test_full_name'
        self.BOT = Bot()

    def test_login(self, monkeypatch):

        def mockreturn(*args, **kwargs):
            r = Mock()
            r.status_code = 200
            r.cookies = {'csrftoken': 'abcdef1234'}
            r.text = '{"status": "ok"}'
            return r

        def mockreturn_login(*args, **kwargs):
            r = Mock()
            r.status_code = 200
            r.cookies = {'csrftoken': 'abcdef1234'}
            r.text = json.dumps({
                "logged_in_user": {
                    "pk": self.USER_ID,
                    "username": self.USERNAME,
                    "full_name": self.FULLNAME
                },
                "status": "ok"
            })
            return r

        monkeypatch.setattr(requests.Session, 'get', mockreturn)
        monkeypatch.setattr(requests.Session, 'post', mockreturn_login)

        self.BOT.login(username=self.USERNAME, password=self.PASSWORD)

        assert self.BOT.username == self.USERNAME
        assert self.BOT.user_id == self.USER_ID
        assert self.BOT.isLoggedIn

    @responses.activate
    def test_logout(self, monkeypatch):
        self.test_login(monkeypatch)
        responses.add(responses.GET, "{API_URL}accounts/logout/".format(
            API_URL=API_URL), json=DEFAULT_RESPONSE, status=200)

        self.BOT.logout()

        assert not self.BOT.isLoggedIn

    def test_set_user(self):
        test_username = "abcdef"
        test_password = "passwordabc"
        self.BOT.setUser(test_username, test_password)

        assert self.BOT.username == test_username
        assert self.BOT.password == test_password
