import time
import datetime
import random
import atexit
import signal
from tqdm import tqdm

from .. import API
from . import limits

from .bot_get_medias import get_timeline_medias
from .bot_get_medias import get_user_medias
from .bot_get_medias import get_hashtag_medias

from .bot_like_feed import like_timeline
from .bot_like_feed import like_user_id
from .bot_like_feed import like_hashtag
from .bot_like_feed import comment_hashtag

from .bot_unfollow_non_followers import unfollow_non_followers
from .bot_follow_followers import follow_followers

from .bot_checkpoint import save_checkpoint
from .bot_checkpoint import load_checkpoint
from .bot_checkpoint import checkpoint_followers_diff
from .bot_checkpoint import checkpoint_following_diff
from .bot_checkpoint import load_last_checkpoint
from .bot_checkpoint import revert_to_checkpoint

from .bot_like_and_follow import like_and_follow
from .bot_like_and_follow import like_and_follow_media_likers
from .bot_like_and_follow import like_and_follow_your_feed_likers

from .bot_comment import get_comment
from .bot_comment import is_commented

from .bot_filter import read_list
from .bot_filter import get_media_owner
from .bot_filter import check_media
from .bot_filter import check_user

class Bot(API):
    def __init__(self,
                 whitelist=False,
                 blacklist=False):
        super(self.__class__, self).__init__()
        self.total_liked = 0
        self.total_unliked = 0
        self.total_followed = 0
        self.total_unfollowed = 0
        self.total_commented = 0
        self.MAX_LIKES_TO_LIKE = limits.MAX_LIKES_TO_LIKE
        self.start_time = datetime.datetime.now()
        self.whitelist = []
        if whitelist:
            self.whitelist = read_list(whitelist)
            print ("Size of whitelist: %d" % len(self.whitelist))
        self.blacklist = []
        if blacklist:
            self.blacklist = read_list(blacklist)
            print ("Size of blacklist: %d" % len(self.blacklist))
        signal.signal(signal.SIGTERM, self.logout)
        atexit.register(self.logout)

    def logout(self):
        super(self.__class__, self).logout()
        print ("Bot stopped. "
               "Worked: %s" % (datetime.datetime.now() - self.start_time))
        if self.total_liked:
            print ("  Total liked: %d" % self.total_liked)
        if self.total_unliked:
            print ("  Total unliked: %d" % self.total_unliked)
        if self.total_followed:
            print ("  Total followed: %d" % self.total_followed)
        if self.total_unfollowed:
            print ("  Total unfollowed: %d" % self.total_unfollowed)
        if self.total_commented:
            print ("  Total commented: %d" % self.total_commented)

    def like(self, media_id):
        if not self.check_media(media_id):
            return False
        if super(self.__class__, self).like(media_id):
            self.total_liked += 1
            return True
        return False

    def unlike(self, media_id):
        if not self.check_media(media_id):
            return False
        if super(self.__class__, self).unlike(media_id):
            self.total_unliked += 1
            return True
        return False

    def follow(self, user_id):
        if not self.check_user(user_id):
            return False
        if super(self.__class__, self).follow(user_id):
            self.total_followed += 1
            return True
        return False

    def unfollow(self, user_id):
        if not self.check_user(user_id):
            return False
        if super(self.__class__, self).unfollow(user_id):
            self.total_unfollowed += 1
            return True
        return False

    def comment(self, media_id, comment_text):
        if not self.check_media(media_id):
            return False
        if super(self.__class__, self).comment(media_id, comment_text):
            self.total_commented += 1
            return True
        return False

    def comment_medias(self, medias):
        """ medias - list of ["pk"] fields of response """
        print ("    Going to comment on %d medias." % (len(medias)))
        total_commented = 0
        for media in tqdm(medias):

            # grab a comment
            co = self.get_comment('comments.txt')

            if self.comment(media, co):
                total_commented += 1
            else:
                pass
            time.sleep(10 * random.random())
        print ("    DONE: Total commented on %d medias. " % total_commented)
        return True


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
        return True

    def get_timeline_medias(self):
        return get_timeline_medias(self)

    def get_user_medias(self, user_id):
        return get_user_medias(self, user_id)

    def like_timeline(self, amount=None):
        return like_timeline(self, amount)

    def like_user_id(self, user_id, amount=None):
        return like_user_id(self, user_id, amount)

    def unfollow_non_followers(self):
        return unfollow_non_followers(self)

    def follow_followers(self, user_id, nfollows=40):
        return follow_followers(self, user_id, nfollows)

    def comment_hashtag(self, tag, ncomments=15):
        return comment_hashtag(self,tag, ncomments)

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

    def get_comment(self, comment_base_file=None):
        return get_comment(self, comment_base_file)

    def is_commented(self, media_id):
        return is_commented(self, media_id)

    def add_whitelist(self, file_path):
        return add_whitelist(self, file_path)

    def add_blacklist(self, file_path):
        return add_blacklist(self, file_path)

    def get_media_owner(self, media):
        return get_media_owner(self, media)

    def check_media(self, media):
        return check_media(self, media)

    def check_user(self, user):
        return check_user(self, user)

    def get_hashtag_medias(self, hashtag, amount=None):
        return get_hashtag_medias(self, hashtag, amount)
