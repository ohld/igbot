import unittest
import logging
from instabot import User
from instabot import API
from instabot import Bot


class TestUser(unittest.TestCase):

    def test_init(self):
        User.delete("test")
        usr = User("test", "testpass")
        usr.save()
        del usr
        usr = User.load("test")
        self.assertEqual(usr.username, "test")
        self.assertEqual(usr.password, "testpass")
        User.delete("test")

    def test_api(self):
        api = API("instabotproject")
        self.assertTrue(api.User.isLoggedIn)
        api.User.save()
        reqs = api.User.counters.requests
        self.assertTrue(api.follow(352300017))
        self.assertTrue(api.unfollow(352300017))
        self.assertEqual(reqs + 2, api.User.counters.requests)
        api.User.save()

    def test_bot(self):
        bot = Bot("instabotproject")
        self.assertTrue(isinstance(bot, Bot))
        reqs = bot.User.counters.requests
        self.assertEqual(bot.convert_to_user_id("ohld"), "352300017")
        self.assertEqual(reqs + 1, bot.User.counters.requests)
        bot.User.save()

def reset_user():
    User.delete("instabotproject")
    api = API("instabotproject")
    api.User.save()

if __name__ == '__main__':
    # reset_user()
    unittest.main()
