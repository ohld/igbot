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
        self.BOT = Bot()
        self.prepare_bot(self.BOT)

    def prepare_bot(self, bot):
        bot.isLoggedIn = True
        bot.user_id = self.USER_ID
        bot.token = 'abcdef123456'
        bot.session = requests.Session()
        bot.setUser(self.USERNAME, self.PASSWORD)
        bot.rank_token = '{}_{}'.format(bot.user_id, bot.uuid)


class TestBotAPI(TestBot):
    def test_login(self):
        self.BOT = Bot()

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

            assert self.BOT.login(username=self.USERNAME,
                                  password=self.PASSWORD)

        assert self.BOT.username == self.USERNAME
        assert self.BOT.user_id == self.USER_ID
        assert self.BOT.isLoggedIn
        assert self.BOT.uuid
        assert self.BOT.token

    def test_logout(self):
        self.BOT.logout()

        assert not self.BOT.isLoggedIn

    def test_generate_uuid(self):
        from uuid import UUID
        generated_uuid = self.BOT.generateUUID(True)

        assert isinstance(UUID(generated_uuid), UUID)
        assert UUID(generated_uuid).hex == generated_uuid.replace('-', '')

    def test_set_user(self):
        test_username = "abcdef"
        test_password = "passwordabc"
        self.BOT.setUser(test_username, test_password)

        assert self.BOT.username == test_username
        assert self.BOT.password == test_password
        assert hasattr(self.BOT, "uuid")

    def test_reset_counters(self):
        from instabot.bot.limits import reset_counters
        counters = ['total_liked', 'total_unliked', 'total_followed',
                    'total_unfollowed', 'total_commented', 'total_blocked', 'total_unblocked']
        for counter in counters:
            setattr(self.BOT, counter, 1)
            assert getattr(self.BOT, counter) is 1

        reset_counters(self.BOT)

        for counter in counters:
            assert getattr(self.BOT, counter) is 0
