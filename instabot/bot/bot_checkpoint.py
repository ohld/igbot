import time
import random
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


def save_checkpoint(bot, path=None):
    """
        Saves bot's checkpoint:
            followers
            following
            date
        Returns the name of saved file
    """
    print ("Saving checkpoint:")
    if path is None:
        path = datetime.now().strftime("bot_cp_%Y-%m-%d_%H-%M")

    cp = Checkpoint()
    cp.fill(bot)

    with open(path, 'wb') as f:
        pickle.dump(cp, f, -1)
    bot.last_checkpoint_path = path
    print ("  Done.")
    return path

def load_checkpoint(bot, path):
    """
        Loads bot's checkpoint
        Returns Checkpoint object
    """
    print ("Loading checkpoint:")
    try:
        with open(path, 'rb') as f:
            cp = pickle.load(f)
        if isinstance(cp, Checkpoint):
            return cp
        else:
            print ("  This is not checkpoint file.")
    except:
        print ("  File not found.")
    return None

def checkpoint_following_diff(bot, cp):
    """
        Returns user_ids of users that you follow now
        but didn't follow at checkpoint time.
    """
    print ("Getting checkpoint following difference.")
    current_following = [item["pk"] for item in bot.getTotalSelfFollowings()]
    old_following = cp.following
    return list(set(current_following) - set(old_following))

def checkpoint_followers_diff(bot, cp):
    """
        Returns user_ids of users that follows you now
        but didn't follow you at checkpoint time.
    """
    print ("Getting checkpoint followers difference.")
    current_followers = [item["pk"] for item in bot.getTotalSelfFollowers()]
    old_following = cp.followers
    return list(set(current_followers) - set(old_followers))

def load_last_checkpoint(bot):
    return bot.load_checkpoint(bot.last_checkpoint_path)

def revert_to_checkpoint(bot, cp):
    return bot.unfollow_users(bot.checkpoint_following_diff(cp))
