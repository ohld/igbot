"""
    Instabot Checkpoint methods.
"""

import os
import pickle
from datetime import datetime

CHECKPOINT_PATH = "{fname}.checkpoint"


class Checkpoint(object):
    """
        Checkpoint for instabot.Bot class which can store:
            .total_<name> - all Bot's counters
            .following (list of user_ids)
            .followers (list of user_ids)
            .date (of checkpoint creation)
    """

    def __init__(self, bot):
        self.total_liked = bot.total_liked
        self.total_unliked = bot.total_unliked
        self.total_followed = bot.total_followed
        self.total_unfollowed = bot.total_unfollowed
        self.total_commented = bot.total_commented
        self.total_blocked = bot.total_blocked
        self.total_unblocked = bot.total_unblocked
        self.total_requests = bot.api.total_requests
        self.start_time = bot.start_time
        self.date = datetime.now()
        self.total_archived = bot.total_archived
        self.total_unarchived = bot.total_unarchived
        self.total_sent_messages = bot.total_sent_messages

    def fill_following(self, bot):
        self.following = [item["pk"] for item in bot.api.get_total_self_followings()]

    def fill_followers(self, bot):
        self.followers = [item["pk"] for item in bot.api.get_total_self_followers()]

    def dump(self):
        return (self.total_liked, self.total_unliked, self.total_followed,
                self.total_unfollowed, self.total_commented, self.total_blocked,
                self.total_unblocked, self.api.total_requests, self.start_time,
                self.total_archived, self.total_unarchived, self.total_sent_messages)


def save_checkpoint(self):
    checkpoint = Checkpoint(self)
    fname = CHECKPOINT_PATH.format(fname=self.api.username)
    with open(fname, 'wb') as f:
        pickle.dump(checkpoint, f, -1)
    return True


def load_checkpoint(self):
    try:
        fname = CHECKPOINT_PATH.format(fname=self.api.username)
        with open(fname, 'rb') as f:
            checkpoint = pickle.load(f)
        if isinstance(checkpoint, Checkpoint):
            return checkpoint.dump()
        else:
            os.remove(fname)
    except Exception:
        pass
    return None
