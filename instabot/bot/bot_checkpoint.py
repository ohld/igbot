"""
    Instabot Checkpoint methods.
"""

import pickle
from datetime import datetime


class Checkpoint(object):
    """
        Checkpoint for instabot.Bot which stores:
            .following (list of user_ids)
            .followers (list of user_ids)
            .date (of checkpoint creation)
    """

    def __init__(self):
        self.following = []
        self.followers = []
        self.date = None

    def fill(self, bot):
        self.following = [item["pk"] for item in bot.getTotalSelfFollowings()]
        self.followers = [item["pk"] for item in bot.getTotalSelfFollowers()]
        self.date = datetime.now()


def save_checkpoint(self, path=None):
    """
        Saves self's checkpoint:
            followers
            following
            date
        Returns the name of saved file
    """
    self.logger.info("Saving checkpoint:")
    if path is None:
        path = datetime.now().strftime("bot_cp_%Y-%m-%d_%H-%M")

    cp = Checkpoint()
    cp.fill(self)

    with open(path, 'wb') as f:
        pickle.dump(cp, f, -1)
    self.last_checkpoint_path = path
    self.logger.info("Done. Your checkpoint is at %s." % path)
    return path


def load_checkpoint(self, path):
    """
        Loads self's checkpoint
        Returns Checkpoint object
    """
    self.logger.info("Loading checkpoint:")
    try:
        with open(path, 'rb') as f:
            cp = pickle.load(f)
        if isinstance(cp, Checkpoint):
            return cp
        else:
            self.logger.info("This is not checkpoint file.")
    except:
        self.logger.info("File not found.")
    return None


def checkpoint_following_diff(self, cp):
    """
        Returns user_ids of users that you follow now
        but didn't follow at checkpoint time.
    """
    self.logger.info("Getting checkpoint following difference.")
    current_following = [item["pk"] for item in self.getTotalSelfFollowings()]
    old_following = cp.following
    return list(set(current_following) - set(old_following))


def checkpoint_followers_diff(self, cp):
    """
        Returns user_ids of users that follows you now
        but didn't follow you at checkpoint time.
    """
    self.logger.info("Getting checkpoint followers difference.")
    current_followers = [item["pk"] for item in self.getTotalSelfFollowers()]
    old_followers = cp.followers
    return list(set(current_followers) - set(old_followers))


def load_last_checkpoint(self):
    return self.load_checkpoint(self.last_checkpoint_path)


def revert_to_checkpoint(self, file_path):
    cp = self.load_checkpoint(file_path)
    if not cp:
        return False
    self.logger.info("Revering to the checkpoint from %s." % cp.date)
    return self.unfollow_users(self.checkpoint_following_diff(cp))
