import datetime

from instaprole.utils.generic_utils.singleton import Singleton
from instaprole.utils.generic_utils.utils import Utils


class BotCache(object, metaclass=Singleton):

    def __init__(self):
        self.following = None
        self.followers = None
        self.user_infos = {}  # User info cache
        self.usernames = {}  # `username` to `user_id` mapping

    def __repr__(self):
        return Utils.get_dict(self)
