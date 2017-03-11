import datetime
import atexit
import signal
import logging

from ..api import API

from .bot_get import get_media_owner, get_your_medias, get_user_medias
from .bot_get import get_timeline_medias, get_hashtag_medias, get_user_info
from .bot_get import get_geotag_medias, get_timeline_users, get_hashtag_users
from .bot_get import get_media_commenters, get_userid_from_username
from .bot_get import get_user_followers, get_user_following, get_media_likers
from .bot_get import get_media_comments, get_geotag_users, convert_to_user_id
from .bot_get import get_comment, get_media_info

from .bot_like import like, like_medias, like_timeline, like_user, like_users
from .bot_like import like_hashtag, like_geotag, like_followers, like_following

from .bot_unlike import unlike, unlike_medias, unlike_user

from .bot_follow import follow, follow_users, follow_followers, follow_following

from .bot_unfollow import unfollow, unfollow_users, unfollow_non_followers
from .bot_unfollow import unfollow_everyone

from .bot_comment import comment, comment_medias, comment_geotag, comment_users
from .bot_comment import comment_hashtag, is_commented

from .bot_block import block, unblock, block_users, unblock_users

from .bot_checkpoint import save_checkpoint, load_checkpoint
from .bot_checkpoint import checkpoint_following_diff, checkpoint_followers_diff
from .bot_checkpoint import load_last_checkpoint, revert_to_checkpoint

from .bot_filter import filter_medias, check_media, filter_users, check_user
from .bot_filter import check_not_bot

from .bot_support import check_if_file_exists, read_list_from_file
from .bot_support import add_whitelist, add_blacklist

from .bot_stats import save_user_stats


class Bot(API):

    def __init__(self,
                 proxy=None,
                 whitelist=False,
                 blacklist=False,
                 comments_file=False,
                 max_likes_per_day=1000,
                 max_unlikes_per_day=1000,
                 max_follows_per_day=350,
                 max_unfollows_per_day=350,
                 max_comments_per_day=100,
                 max_blocks_per_day=100,
                 max_unblocks_per_day=100,
                 max_likes_to_like=100,
                 max_followers_to_follow=2000,
                 min_followers_to_follow=10,
                 max_following_to_follow=10000,
                 min_following_to_follow=10,
                 max_followers_to_following_ratio=10,
                 max_following_to_followers_ratio=2,
                 min_media_count_to_follow=3,
                 like_delay=10,
                 unlike_delay=10,
                 follow_delay=30,
                 unfollow_delay=30,
                 comment_delay=60,
                 block_delay=30,
                 unblock_delay=30,
                 stop_words=['shop', 'store', 'free']):
        super(self.__class__, self).__init__()

        self.total_liked = 0
        self.total_unliked = 0
        self.total_followed = 0
        self.total_unfollowed = 0
        self.total_commented = 0
        self.total_blocked = 0
        self.total_unblocked = 0
        self.start_time = datetime.datetime.now()

        # limits
        self.max_likes_per_day = max_likes_per_day
        self.max_unlikes_per_day = max_unlikes_per_day
        self.max_follows_per_day = max_follows_per_day
        self.max_unfollows_per_day = max_unfollows_per_day
        self.max_comments_per_day = max_comments_per_day
        self.max_blocks_per_day = max_blocks_per_day
        self.max_unblocks_per_day = max_unblocks_per_day
        self.max_likes_to_like = max_likes_to_like
        self.max_followers_to_follow = max_followers_to_follow
        self.min_followers_to_follow = min_followers_to_follow
        self.max_following_to_follow = max_following_to_follow
        self.min_following_to_follow = min_following_to_follow
        self.max_followers_to_following_ratio = max_followers_to_following_ratio
        self.max_following_to_followers_ratio = max_following_to_followers_ratio
        self.min_media_count_to_follow = min_media_count_to_follow
        self.stop_words = stop_words

        # delays
        self.like_delay = like_delay
        self.unlike_delay = unlike_delay
        self.follow_delay = follow_delay
        self.unfollow_delay = unfollow_delay
        self.comment_delay = comment_delay
        self.block_delay = block_delay
        self.unblock_delay = unblock_delay

        # handle logging
        self.logger = logging.getLogger('[instabot]')
        self.logger.setLevel(logging.DEBUG)
        logging.basicConfig(format='%(asctime)s %(message)s',
                            filename='instabot.log',
                            level=logging.INFO
                            )
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.logger.info('Instabot Started')

        # current following
        self.following = []

        # white and blacklists
        self.whitelist = []
        if whitelist:
            self.whitelist = read_list_from_file(whitelist)
        self.blacklist = []
        if blacklist:
            self.blacklist = read_list_from_file(blacklist)

        # comment file
        self.comments = []
        if comments_file:
            self.comments = read_list_from_file(comments_file)

        signal.signal(signal.SIGTERM, self.logout)
        atexit.register(self.logout)

    def logout(self):
        super(self.__class__, self).logout()
        self.logger.info("Bot stopped. "
                         "Worked: %s" % (datetime.datetime.now() - self.start_time))
        if self.total_liked:
            self.logger.info("Total liked: %d" % self.total_liked)
        if self.total_unliked:
            self.logger.info("Total unliked: %d" % self.total_unliked)
        if self.total_followed:
            self.logger.info("Total followed: %d" % self.total_followed)
        if self.total_unfollowed:
            self.logger.info("Total unfollowed: %d" % self.total_unfollowed)
        if self.total_commented:
            self.logger.info("Total commented: %d" % self.total_commented)
        if self.total_blocked:
            self.logger.info("Total blocked: %d" % self.total_blocked)
        if self.total_unblocked:
            self.logger.info("Total unblocked: %d" % self.total_unblocked)

    def login(self, *args):
        super(self.__class__, self).login(args)
        self.prepare()

    def prepare(self):
        self.whitelist = [
            self.convert_to_user_id(smth) for smth in self.whitelist]
        self.blacklist = [
            self.convert_to_user_id(smth) for smth in self.blacklist]

    # getters

    def get_your_medias(self):
        return get_your_medias(self)

    def get_timeline_medias(self):
        return get_timeline_medias(self)

    def get_user_medias(self, user_id, filtration=True):
        return get_user_medias(self, user_id, filtration)

    def get_hashtag_medias(self, hashtag, filtration=True):
        return get_hashtag_medias(self, hashtag, filtration)

    def get_geotag_medias(self, geotag, filtration=True):
        return get_geotag_medias(self, geotag, filtration)

    def get_media_info(self, media_id):
        return get_media_info(self, media_id)

    def get_timeline_users(self):
        return get_timeline_users(self)

    def get_hashtag_users(self, hashtag):
        return get_hashtag_users(self, hashtag)

    def get_geotag_users(self, geotag):
        return get_geotag_users(self, geotag)

    def get_userid_from_username(self, username):
        return get_userid_from_username(self, username)

    def get_user_info(self, user_id):
        return get_user_info(self, user_id)

    def get_user_followers(self, user_id):
        return get_user_followers(self, user_id)

    def get_user_following(self, user_id):
        return get_user_following(self, user_id)

    def get_media_likers(self, media_id):
        return get_media_likers(self, media_id)

    def get_media_comments(self, media_id):
        return get_media_comments(self, media_id)

    def get_comment(self):
        return get_comment(self)

    def get_media_commenters(self, media_id):
        return get_media_commenters(self, media_id)

    def get_media_owner(self, media):
        return get_media_owner(self, media)

    def convert_to_user_id(self, usernames):
        return convert_to_user_id(self, usernames)

    # like

    def like(self, media_id):
        return like(self, media_id)

    def like_medias(self, media_ids):
        return like_medias(self, media_ids)

    def like_timeline(self, amount=None):
        return like_timeline(self, amount)

    def like_user(self, user_id, amount=None):
        return like_user(self, user_id, amount)

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

    def unlike_user(self, user):
        return unlike_user(self, user)

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

    # block

    def block(self, user_id):
        return block(self, user_id)

    def unblock(self, user_id):
        return unblock(self, user_id)

    def block_users(self, user_ids):
        return block_users(self, user_ids)

    def unblock_users(self, user_ids):
        return unblock_users(self, user_ids)

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

    def filter_medias(self, media_items, filtration=True):
        return filter_medias(self, media_items, filtration)

    def check_media(self, media):
        return check_media(self, media)

    def check_user(self, user):
        return check_user(self, user)

    def check_not_bot(self, user):
        return check_not_bot(self, user)

    def filter_users(self, user_id_list):
        return filter_users(self, user_id_list)

    # support

    def check_if_file_exists(self, file_path):
        return check_if_file_exists(file_path)

    def read_list_from_file(self, file_path):
        return read_list_from_file(file_path)

    def add_whitelist(self, file_path):
        return add_whitelist(self, file_path)

    def add_blacklist(self, file_path):
        return add_blacklist(self, file_path)

    # stats

    def save_user_stats(self, username):
        return save_user_stats(self, username)
