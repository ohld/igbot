import time
import random
from tqdm import tqdm

from .. import API

from .bot_like_feed import like_timeline
from .bot_like_feed import like_user_id
from .bot_unfollow_non_followers import unfollow_non_followers
from .bot_like_hashtag import like_hashtag

from .bot_checkpoint import save_checkpoint
from .bot_checkpoint import load_checkpoint
from .bot_checkpoint import checkpoint_followers_diff
from .bot_checkpoint import checkpoint_following_diff
from .bot_checkpoint import load_last_checkpoint
from .bot_checkpoint import revert_to_checkpoint

from .bot_like_and_follow import like_and_follow
from .bot_like_and_follow import like_and_follow_media_likers
from .bot_like_and_follow import like_and_follow_your_feed_likers

class Bot(API):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.total_liked = 0
        self.total_followed = 0
        self.total_unfollowed = 0

    def logout(self):
        super(self.__class__, self).logout()
        print ("""Bot stopped.
                  Total liked: %d,
                  Total followed: %d,
                  Total unfollowed: %d""" % (
            self.total_liked, self.total_followed, self.total_unfollowed
        ))

    def like_medias(self, medias):
        """ medias - list of ["pk"] fields of response """
        print ("    Going to like %d medias." % (len(medias)))
        total_liked = 0
        for media in tqdm(medias):
            if self.like(media):
                total_liked += 1
            else:
                pass
            time.sleep(10 * random.random())
        print ("    DONE: Total liked %d medias. " % total_liked)
        self.total_liked += total_liked
        return True

    def follow_users(self, user_ids):
        """ user_ids - list of user_id to follow """
        print ("    Going to follow %d users." % len(user_ids))
        total_followed = 0
        for user_id in tqdm(user_ids):
            if self.follow(user_id):
                total_followed += 1
            else:
                pass
            time.sleep(15 + 30 * random.random())
        print ("    DONE: Total followed %d users. " % total_followed)
        self.total_followed += total_followed
        return True

    def unfollow_users(self, user_ids):
        """ user_ids - list of user_id to unfollow """
        print ("    Going to unfollow %d users." % len(user_ids))
        total_unfollowed = 0
        for user_id in tqdm(user_ids):
            if self.unfollow(user_id):
                total_unfollowed += 1
            else:
                pass
            time.sleep(15 + 30 * random.random())
        print ("    DONE: Total unfollowed %d users. " % total_unfollowed)
        self.total_unfollowed += total_unfollowed
        return True

    def like_timeline(self, amount=None):
        return like_timeline(self, amount)

    def like_user_id(self, user_id, amount=None):
        return like_user_id(self, user_id, amount)

    def unfollow_non_followers(self):
        return unfollow_non_followers(self)

    def like_hashtag(self, tag, amount=None):
        return like_hashtag(self, tag, amount)

    def save_checkpoint(self):
        return save_checkpoint(self)

    def load_checkpoint(self, path):
        return load_checkpoint(self, path)

    def checkpoint_followers_diff(self, cp):
        return checkpoint_followers_diff(self, cp)

    def checkpoint_following_diff(self, cp):
        return checkpoint_following_diff(self, cp)

    def load_last_checkpoint(self):
        return load_last_checkpoint(self)

    def revert_to_checkpoint(self, cp):
        return revert_to_checkpoint(self, cp)

    def like_and_follow(self, user_id, nlikes=3):
        return like_and_follow(self, user_id, nlikes)

    def like_and_follow_media_likers(self, media, nlikes=3):
        return like_and_follow_media_likers(self, media, nlikes)

    def like_and_follow_your_feed_likers(self, nlikes=3):
        return like_and_follow_your_feed_likers(self, nlikes)
