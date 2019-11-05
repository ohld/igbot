import datetime

from instaprole.data.mongo.mongo_object import MongoObject
from instaprole.utils.generic_utils.singleton import Singleton
from instaprole.utils.generic_utils.utils import Utils
from instaprole.utils.time_utils.datetime_utils import DatetimeUtils


class BotState(MongoObject, metaclass=Singleton):

    def __init__(self):
        self.start_time = DatetimeUtils.now()
        self.total = dict.fromkeys([
            "likes",
            "unlikes",
            "follows",
            "unfollows",
            "comments",
            "blocks",
            "unblocks",
            "messages",
            "archived",
            "unarchived",
            "stories_viewed",
        ], 0)
        self.blocked_actions = dict.fromkeys([
            "likes",
            "unlikes",
            "follows",
            "unfollows",
            "comments",
            "blocks",
            "unblocks",
            "messages"
        ], False)
        self.last_action_time = dict.fromkeys([
            "like",
            "unlike",
            "follow",
            "unfollow",
            "comment",
            "block",
            "unblock",
            "message",
        ], 0)

    def increment_total(self, key):
        self.total[key] += 1

    def reset_state(self):
        for k in self.total:
            self.total[k] = 0
        for k in self.last_action_time:
            self.last_action_time[k] = 0
        for k in self.blocked_actions:
            self.blocked_actions[k] = False
        self.start_time = DatetimeUtils.now()

    def get_total(self, key):
        return self.total[key]

    def __repr__(self):
        return Utils.get_dict(self)

