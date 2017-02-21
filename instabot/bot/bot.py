import os
import sys
import datetime
import atexit
import signal
import logging
import io

from tqdm import tqdm

from .. import API
from . import limits

from .bot_get import get_your_medias
from .bot_get import get_timeline_medias
from .bot_get import get_user_medias
from .bot_get import get_hashtag_medias
from .bot_get import get_geotag_medias
from .bot_get import get_timeline_users
from .bot_get import get_hashtag_users
from .bot_get import get_geotag_users
from .bot_get import get_userid_from_username
from .bot_get import get_user_followers
from .bot_get import get_user_following
from .bot_get import get_media_likers
from .bot_get import get_media_comments
from .bot_get import get_comment
from .bot_get import get_media_commenters

from .bot_like import like
from .bot_like import like_medias
from .bot_like import like_timeline
from .bot_like import like_user_id
from .bot_like import like_hashtag
from .bot_like import like_geotag
from .bot_like import like_users
from .bot_like import like_followers
from .bot_like import like_following

from .bot_unlike import unlike
from .bot_unlike import unlike_medias

from .bot_follow import follow
from .bot_follow import follow_users
from .bot_follow import follow_followers
from .bot_follow import follow_following

from .bot_unfollow import unfollow
from .bot_unfollow import unfollow_users
from .bot_unfollow import unfollow_non_followers
from .bot_unfollow import unfollow_everyone

from .bot_comment import comment
from .bot_comment import comment_hashtag
from .bot_comment import comment_users
from .bot_comment import comment_geotag
from .bot_comment import comment_medias
from .bot_comment import is_commented

from .bot_checkpoint import save_checkpoint
from .bot_checkpoint import load_checkpoint
from .bot_checkpoint import checkpoint_followers_diff
from .bot_checkpoint import checkpoint_following_diff
from .bot_checkpoint import load_last_checkpoint
from .bot_checkpoint import revert_to_checkpoint

from .bot_filter import check_if_file_exists
from .bot_filter import read_list_from_file
from .bot_filter import get_media_owner
from .bot_filter import check_media
from .bot_filter import check_user
from .bot_filter import convert_to_user_id

class Bot(API):
    def __init__(self,
                 whitelist=False,
                 blacklist=False,
                 comments_file=False,
                 max_likes_per_day=1000,
                 max_follows_per_day=350,
                 max_unfollows_per_day=350,
                 max_comments_per_day=100,
                 like_delay=10,
                 follow_delay=30,
                 unfollow_delay=30,
                 comment_delay=60):
        super(self.__class__, self).__init__()

        self.total_liked = 0
        self.total_unliked = 0
        self.total_followed = 0
        self.total_unfollowed = 0
        self.total_commented = 0
        self.start_time = datetime.datetime.now()

        # limits
        self.max_likes_per_day = max_likes_per_day
        self.max_follows_per_day = max_follows_per_day
        self.max_unfollows_per_day = max_unfollows_per_day
        self.max_comments_per_day = max_comments_per_day

        # delays
        self.like_delay = like_delay
        self.follow_delay = follow_delay
        self.unfollow_delay = unfollow_delay
        self.comment_delay = comment_delay

        # handle logging
        self.logger = logging.getLogger('[instabot]')
        self.logger.setLevel(logging.DEBUG)
        logging.basicConfig(format='%(asctime)s %(message)s', filename='instabot.log', level=logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.logger.info('Instabot Started')

        # current following
        self.following = []

        # white and blacklists
        self.whitelist = []
        if whitelist:
            self.whitelist = read_list_from_file(whitelist)
            self.logger.info("Size of whitelist: %d" % len(self.whitelist))
        self.blacklist = []
        if blacklist:
            self.blacklist = read_list_from_file(blacklist)
            self.logger.info("Size of blacklist: %d" % len(self.blacklist))
        signal.signal(signal.SIGTERM, self.logout)
        atexit.register(self.logout)

        # comment file
        self.comments = []
        if comments_file:
            if os.path.exists(comments_file):
                with io.open(comments_file, "r", encoding="utf8") as f:
                    self.comments = f.readlines()
            else:
                self.logger.info("Can't find comment file!")

    def logout(self):
        super(self.__class__, self).logout()
        self.logger.info("Bot stopped. "
               "Worked: %s" % (datetime.datetime.now() - self.start_time))
        if self.total_liked:
            self.logger.info("  Total liked: %d" % self.total_liked)
        if self.total_unliked:
            self.logger.info("  Total unliked: %d" % self.total_unliked)
        if self.total_followed:
            self.logger.info("  Total followed: %d" % self.total_followed)
        if self.total_unfollowed:
            self.logger.info("  Total unfollowed: %d" % self.total_unfollowed)
        if self.total_commented:
            self.logger.info("  Total commented: %d" % self.total_commented)

# getters

    def get_your_medias(self):
        return get_your_medias(self)

    def get_timeline_medias(self):
        return get_timeline_medias(self)

    def get_user_medias(self, user_id):
        return get_user_medias(self, user_id)

    def get_hashtag_medias(self, hashtag):
        return get_hashtag_medias(self, hashtag)

    def get_geotag_medias(self, geotag):
        return get_geotag_medias(self, geotag)

    def get_timeline_users(self):
        return get_timeline_users(self)

    def get_hashtag_users(self, hashtag):
        return get_hashtag_users(self, hashtag)

    def get_geotag_users(self, geotag):
        return get_geotag_users(self, geotag)

    def get_userid_from_username(self, username):
        return get_userid_from_username(self, username)

    def get_user_followers(self, user_id):
        return get_user_followers(self, user_id)

    def get_user_following(self, user_id):
        return get_user_following(self, user_id)

    def get_media_likers(self, media_id):
        return get_media_likers(self, media_id)

    def get_media_comments(self, media_id):
        return get_media_likers(self, media_id)

    def get_comment(self):
        return get_comment(self)

    def get_media_commenters(bot, media_id):
        return get_media_commenters(bot, media_id)

# like

    def like(self, media_id):
        return like(self, media_id)

    def like_medias(self, media_ids):
        return like_medias(self, media_ids)

    def like_timeline(self, amount=None):
        return like_timeline(self, amount)

    def like_user_id(self, user_id, amount=None):
        return like_user_id(self, user_id, amount)

    def like_hashtag(self, hashtag, amount=None):
        return like_hashtag(self, hashtag, amount)

    def like_geotag(self, geotag, amount=None):
        return like_geotag(self, geotag, amount)

    def like_users(self, user_ids, nlikes=None):
        return like_users(self, user_ids, nlikes)

    def like_followers(self, user_id, nlikes=None):
        return like_followers(self, user_id, nlikes)

    def like_following(self, user_id, nlikes=None):
        return like_following(self, user_id, nlikes)

# unlike

    def unlike(self, media_id):
        return unlike(self, media_id)

    def unlike_medias(self, media_ids):
        return unlike_medias(self, media_ids)

# follow

    def follow(self, user_id):
        return follow(self, user_id)

    def follow_users(self, user_ids):
        return follow_users(self, user_ids)

    def follow_followers(self, user_id):
        return follow_followers(self, user_id)

    def follow_following(self, user_id):
        return follow_following(self, user_id)

# unfollow

    def unfollow(self, user_id):
        return unfollow(self, user_id)

    def unfollow_users(self, user_ids):
        return unfollow_users(self, user_ids)

    def unfollow_non_followers(self):
        return unfollow_non_followers(self)

    def unfollow_everyone(self):
        return unfollow_everyone(self)

# comment

    def comment(self, media_id, comment_text):
        return comment(self, media_id, comment_text)

    def comment_hashtag(self, hashtag):
        return comment_hashtag(self, hashtag)

    def comment_medias(self, medias):
        return comment_medias(self, medias)

    def comment_users(self, user_ids):
        return comment_users(self, user_ids)

    def comment_geotag(self, geotag):
        return comment_geotag(self, geotag)

    def is_commented(self, media_id):
        return is_commented(self, media_id)

# checkpoint

    def save_checkpoint(self, path=None):
        return save_checkpoint(self, path)

    def load_checkpoint(self, path):
        return load_checkpoint(self, path)

    def checkpoint_followers_diff(self, cp):
        return checkpoint_followers_diff(self, cp)

    def checkpoint_following_diff(self, cp):
        return checkpoint_following_diff(self, cp)

    def load_last_checkpoint(self):
        return load_last_checkpoint(self)

    def revert_to_checkpoint(self, file_path):
        return revert_to_checkpoint(self, file_path)

# filter

    def check_if_file_exists(self, file_path):
        return check_if_file_exists(file_path)

    def read_list_from_file(self, file_path):
        return read_list_from_file(file_path)

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

    def convert_to_user_id(self, usernames):
        return convert_to_user_id(self, usernames)
