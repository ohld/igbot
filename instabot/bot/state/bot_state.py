import datetime

from instabot.singleton import Singleton


class BotState(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.start_time = datetime.datetime.now()
        self.total = dict.fromkeys(
            [
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
            ],
            0,
        )
        self.blocked_actions = dict.fromkeys(
            [
                "likes",
                "unlikes",
                "follows",
                "unfollows",
                "comments",
                "blocks",
                "unblocks",
                "messages",
            ],
            False,
        )
        self.sleeping_actions = dict.fromkeys(
            [
                "likes",
                "unlikes",
                "follows",
                "unfollows",
                "comments",
                "blocks",
                "unblocks",
                "messages",
            ],
            False,
        )
        self.last = dict.fromkeys(
            [
                "like",
                "unlike",
                "follow",
                "unfollow",
                "comment",
                "block",
                "unblock",
                "message",
            ],
            0,
        )

    def __repr__(self):
        return self.__dict__
