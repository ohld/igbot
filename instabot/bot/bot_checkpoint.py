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
            .total[<name>] - all Bot's counters
            .following (list of user_ids)
            .followers (list of user_ids)
            .date (of checkpoint creation)
    """

    def __init__(self, bot):
        for k in bot.total:
            self.total[k] = bot.total[k]
        self.start_time = bot.start_time
        self.date = datetime.now()

    def fill_following(self, bot):
        self._following = [item["pk"] for item in bot.api.get_total_self_followings()]

    def fill_followers(self, bot):
        self._followers = [item["pk"] for item in bot.api.get_total_self_followers()]

    def dump(self):
        return (self.total, self.start_time)


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
