import json
from unittest.mock import Mock

import requests

from instabot import Bot


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
