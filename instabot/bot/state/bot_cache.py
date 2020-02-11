from instabot.singleton import Singleton


class BotCache(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.following = None
        self.followers = None
        self.user_infos = {}  # User info cache
        self.usernames = {}  # `username` to `user_id` mapping

    def __repr__(self):
        return self.__dict__
