import json
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch

import requests

from instabot import Bot


class TestBot:
    def setup(self):
        self.USER_ID = 1234567
        self.USERNAME = 'test_username'
        self.PASSWORD = 'test_password'
        self.FULLNAME = 'test_full_name'
        self.bot = Bot()
        self.prepare_api(self.bot)

    def prepare_api(self, bot):
        bot.api.is_logged_in = True
        bot.api.user_id = self.USER_ID
        bot.api.token = 'abcdef123456'
        bot.api.session = requests.Session()
        bot.api.set_user(self.USERNAME, self.PASSWORD)
        bot.api.rank_token = '{}_{}'.format(bot.api.user_id, bot.api.uuid)


class TestBotAPI(TestBot):
    def test_login(self):
        self.bot = Bot()

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

        with patch('requests.Session') as Session:
            instance = Session.return_value
            instance.get.return_value = mockreturn()
            instance.post.return_value = mockreturn_login()

            assert self.bot.api.login(username=self.USERNAME,
                                      password=self.PASSWORD)

        assert self.bot.api.username == self.USERNAME
        assert self.bot.user_id == self.USER_ID
        assert self.bot.api.is_logged_in
        assert self.bot.api.uuid
        assert self.bot.api.token

    def test_logout(self):
        self.bot.logout()

        assert not self.bot.api.is_logged_in

    def test_generate_uuid(self):
        from uuid import UUID
        generated_uuid = self.bot.api.generate_UUID(True)

        assert isinstance(UUID(generated_uuid), UUID)
        assert UUID(generated_uuid).hex == generated_uuid.replace('-', '')

    def test_set_user(self):
        test_username = "abcdef"
        test_password = "passwordabc"
        self.bot.api.set_user(test_username, test_password)

        assert self.bot.api.username == test_username
        assert self.bot.api.password == test_password
        assert hasattr(self.bot.api, "uuid")

    def test_reset_counters(self):
        keys = ['liked', 'unliked', 'followed',
                'unfollowed', 'commented', 'blocked', 'unblocked']
        for key in keys:
            self.bot.total[key] = 1
            assert self.bot.total[key] == 1
        self.bot.reset_counters()
        for key in keys:
            assert self.bot.total[key] == 0
