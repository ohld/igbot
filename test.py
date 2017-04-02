import unittest
from instabot import User
from instabot import API


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
        print(api.User.dump())
        print(api.User.counters)


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

if __name__ == '__main__':
    unittest.main()
