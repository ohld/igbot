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
        self.assertTrue(api.follow("352300017"))
        self.assertTrue(api.unfollow("352300017"))
        self.assertEqual(reqs + 2, api.User.counters.requests)

    def test_bot(self):
        bot = Bot("instabotproject")
        self.assertTrue(isinstance(bot, Bot))


    # def test_upper(self):
    #     self.assertEqual('foo'.upper(), 'FOO')
    #
    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())
    #
    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

def update_user():
    User.delete("instabotproject")
    api = API("instabotproject", "")
    api.User.save()

if __name__ == '__main__':
    # update_user()
    logger = logging.getLogger('[instabot]')
    logger.propagate = False
    unittest.main()
