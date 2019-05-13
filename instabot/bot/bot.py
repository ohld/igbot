import os
import atexit
import datetime
import random
import signal
import time

from .. import utils
from ..api import API
from .bot_archive import archive, archive_medias, unarchive_medias
from .bot_block import block, block_bots, block_users, unblock, unblock_users
from .bot_checkpoint import load_checkpoint, save_checkpoint
from .bot_comment import (comment, comment_geotag, comment_hashtag,
                          comment_medias, comment_user, comment_users,
                          is_commented, reply_to_comment)
from .bot_delete import delete_comment, delete_media, delete_medias
from .bot_direct import (send_hashtag, send_like, send_media, send_medias,
                         send_message, send_messages, send_profile,
                         approve_pending_thread_requests)
from .bot_filter import check_media, check_not_bot, check_user, filter_medias
from .bot_follow import (follow, follow_followers, follow_following,
                         follow_users, approve_pending_follow_requests, reject_pending_follow_requests)
from .bot_get import (convert_to_user_id, get_archived_medias, get_comment,
                      get_comment_likers, get_geotag_medias, get_geotag_users,
                      get_hashtag_medias, get_hashtag_users,
                      get_last_user_medias, get_locations_from_coordinates,
                      get_media_commenters, get_media_comments,
                      get_media_comments_all, get_media_id_from_link,
                      get_link_from_media_id, get_media_info, get_media_likers,
                      get_media_owner, get_messages, get_popular_medias,
                      get_timeline_medias, get_timeline_users,
                      get_total_hashtag_medias, get_total_user_medias,
                      get_user_followers, get_user_following,
                      get_user_id_from_username, get_user_info,
                      get_user_likers, get_user_medias, get_user_tags_medias,
                      get_username_from_user_id, get_your_medias, search_users,
                      get_user_stories, get_user_reel, get_self_story_viewers,
                      get_pending_follow_requests, get_pending_thread_requests)
from .bot_like import (like, like_comment, like_followers, like_following,
                       like_geotag, like_hashtag, like_media_comments,
                       like_medias, like_timeline, like_user, like_users, like_location_feed)
from .bot_photo import download_photo, download_photos, upload_photo
from .bot_stats import save_user_stats
from .bot_support import (check_if_file_exists, console_print, extract_urls,
                          read_list_from_file)
from .bot_unfollow import (unfollow, unfollow_everyone, unfollow_non_followers,
                           unfollow_users)
from .bot_unlike import (unlike, unlike_comment, unlike_media_comments,
                         unlike_medias, unlike_user)
from .bot_video import upload_video, download_video
from .bot_story import download_stories, upload_story_photo


class Bot(object):
    def __init__(self,
                 whitelist_file='whitelist.txt',
                 blacklist_file='blacklist.txt',
                 comments_file='comments.txt',
                 followed_file='followed.txt',
                 unfollowed_file='unfollowed.txt',
                 skipped_file='skipped.txt',
                 friends_file='friends.txt',
                 base_path='',
                 proxy=None,
                 max_likes_per_day=1000,
                 max_unlikes_per_day=1000,
                 max_follows_per_day=350,
                 max_unfollows_per_day=350,
                 max_comments_per_day=100,
                 max_blocks_per_day=100,
                 max_unblocks_per_day=100,
                 max_likes_to_like=100,
                 min_likes_to_like=20,
                 max_messages_per_day=300,
                 filter_users=True,
                 filter_private_users=True,
                 filter_users_without_profile_photo=True,
                 filter_previously_followed=False,
                 filter_business_accounts=True,
                 filter_verified_accounts=True,
                 max_followers_to_follow=2000,
                 min_followers_to_follow=10,
                 max_following_to_follow=2000,
                 min_following_to_follow=10,
                 max_followers_to_following_ratio=10,
                 max_following_to_followers_ratio=2,
                 min_media_count_to_follow=3,
                 max_following_to_block=2000,
                 like_delay=10,
                 unlike_delay=10,
                 follow_delay=30,
                 unfollow_delay=30,
                 comment_delay=60,
                 block_delay=30,
                 unblock_delay=30,
                 message_delay=60,
                 stop_words=('shop', 'store', 'free'),
                 blacklist_hashtags=['#shop', '#store', '#free'],
                 blocked_actions_protection=True,
                 verbosity=True,
                 device=None
                 ):
        self.api = API(device=device, base_path=base_path)
        self.base_path = base_path

        self.total = {'likes': 0,
                      'unlikes': 0,
                      'follows': 0,
                      'unfollows': 0,
                      'comments': 0,
                      'blocks': 0,
                      'unblocks': 0,
                      'messages': 0,
                      'archived': 0,
                      'unarchived': 0}

        self.start_time = datetime.datetime.now()

        self.delays = {'like': like_delay,
                       'unlike': unlike_delay,
                       'follow': follow_delay,
                       'unfollow': unfollow_delay,
                       'comment': comment_delay,
                       'block': block_delay,
                       'unblock': unblock_delay,
                       'message': message_delay}

        self.last = {key: 0 for key in self.delays.keys()}

        # limits - follow
        self.filter_users = filter_users
        self.filter_private_users = filter_private_users
        self.filter_users_without_profile_photo = filter_users_without_profile_photo
        self.filter_business_accounts = filter_business_accounts
        self.filter_verified_accounts = filter_verified_accounts
        self.filter_previously_followed = filter_previously_followed

        self.max_per_day = {'likes': max_likes_per_day,
                            'unlikes': max_unlikes_per_day,
                            'follows': max_follows_per_day,
                            'unfollows': max_unfollows_per_day,
                            'comments': max_comments_per_day,
                            'blocks': max_blocks_per_day,
                            'unblocks': max_unblocks_per_day,
                            'messages': max_messages_per_day}

        self.blocked_actions_protection = blocked_actions_protection

        self.blocked_actions = {'likes': False,
                                'unlikes': False,
                                'follows': False,
                                'unfollows': False,
                                'comments': False,
                                'blocks': False,
                                'unblocks': False,
                                'messages': False}

        self.max_likes_to_like = max_likes_to_like
        self.min_likes_to_like = min_likes_to_like
        self.max_followers_to_follow = max_followers_to_follow
        self.min_followers_to_follow = min_followers_to_follow
        self.max_following_to_follow = max_following_to_follow
        self.min_following_to_follow = min_following_to_follow
        self.max_followers_to_following_ratio = max_followers_to_following_ratio
        self.max_following_to_followers_ratio = max_following_to_followers_ratio
        self.min_media_count_to_follow = min_media_count_to_follow
        self.stop_words = stop_words
        self.blacklist_hashtags = blacklist_hashtags

        # limits - block
        self.max_following_to_block = max_following_to_block

        # current following and followers
        self._following = None
        self._followers = None
        self._user_infos = {}  # User info cache
        self._usernames = {}  # `username` to `user_id` mapping

        # Adjust file paths
        followed_file = os.path.join(base_path, followed_file)
        unfollowed_file = os.path.join(base_path, unfollowed_file)
        skipped_file = os.path.join(base_path, skipped_file)
        friends_file = os.path.join(base_path, friends_file)
        comments_file = os.path.join(base_path, comments_file)
        blacklist_file = os.path.join(base_path, blacklist_file)
        whitelist_file = os.path.join(base_path, whitelist_file)

        # Database files
        self.followed_file = utils.file(followed_file)
        self.unfollowed_file = utils.file(unfollowed_file)
        self.skipped_file = utils.file(skipped_file)
        self.friends_file = utils.file(friends_file)
        self.comments_file = utils.file(comments_file)
        self.blacklist_file = utils.file(blacklist_file)
        self.whitelist_file = utils.file(whitelist_file)

        self.proxy = proxy
        self.verbosity = verbosity

        self.logger = self.api.logger
        self.logger.info('Instabot Started')

    @property
    def user_id(self):
        # For compatibility
        return self.api.user_id

    @property
    def username(self):
        # For compatibility
        return self.api.username

    @property
    def password(self):
        # For compatibility
        return self.api.password

    @property
    def last_json(self):
        # For compatibility
        return self.api.last_json

    @property
    def blacklist(self):
        # This is a fast operation because `get_user_id_from_username` is cached.
        return [self.convert_to_user_id(i) for i in self.blacklist_file.list
                if i is not None]

    @property
    def whitelist(self):
        # This is a fast operation because `get_user_id_from_username` is cached.
        return [self.convert_to_user_id(i) for i in self.whitelist_file.list
                if i is not None]

    @property
    def following(self):
        now = time.time()
        last = self.last.get('updated_following', now)
        if self._following is None or now - last > 7200:
            self.console_print('`bot.following` is empty, will download.', 'green')
            self._following = self.get_user_following(self.user_id)
            self.last['updated_following'] = now
        return self._following

    @property
    def followers(self):
        now = time.time()
        last = self.last.get('updated_followers', now)
        if self._followers is None or now - last > 7200:
            self.console_print('`bot.followers` is empty, will download.', 'green')
            self._followers = self.get_user_followers(self.user_id)
            self.last['updated_followers'] = now
        return self._followers

    def version(self):
        try:
            from pip._vendor import pkg_resources
        except ImportError:
            import pkg_resources
        return next((p.version for p in pkg_resources.working_set if p.project_name.lower() == 'instabot'), "No match")

    def logout(self, *args, **kwargs):
        save_checkpoint(self)
        self.api.logout()
        self.logger.info("Bot stopped. "
                         "Worked: %s", datetime.datetime.now() - self.start_time)
        self.print_counters()

    def login(self, **args):
        if self.proxy:
            args['proxy'] = self.proxy
        if self.api.login(**args) is False:
            return False
        self.prepare()
        signal.signal(signal.SIGTERM, self.logout)
        atexit.register(self.logout)
        return True

    def prepare(self):
        storage = load_checkpoint(self)
        if storage is not None:
            self.total, self.blocked_actions, self.api.total_requests, self.start_time = storage

    def print_counters(self):
        for key, val in self.total.items():
            if val > 0:
                self.logger.info("Total {}: {}{}".format(key, val,
                                                         "/" + str(self.max_per_day[key]) if self.max_per_day.get(key) else ""))
        for key, val in self.blocked_actions.items():
            if val:
                self.logger.info("Blocked {}".format(key))
        self.logger.info("Total requests: {}".format(self.api.total_requests))

    def delay(self, key):
        """Sleep only if elapsed time since `self.last[key]` < `self.delay[key]`."""
        last_action, target_delay = self.last[key], self.delays[key]
        elapsed_time = time.time() - last_action
        if elapsed_time < target_delay:
            t_remaining = target_delay - elapsed_time
            time.sleep(t_remaining * random.uniform(0.25, 1.25))
        self.last[key] = time.time()

    def error_delay(self):
        time.sleep(10)

    def small_delay(self):
        time.sleep(random.uniform(0.75, 3.75))

    def very_small_delay(self):
        time.sleep(random.uniform(0.175, 0.875))

    def reached_limit(self, key):
        current_date = datetime.datetime.now()
        passed_days = (current_date.date() - self.start_time.date()).days
        if passed_days > 0:
            self.reset_counters()
        return self.max_per_day[key] - self.total[key] <= 0

    def reset_counters(self):
        for k in self.total:
            self.total[k] = 0
        for k in self.blocked_actions:
            self.blocked_actions[k] = False
        self.start_time = datetime.datetime.now()

    # getters
    def get_user_stories(self, user_id):
        """
        Returns array of stories links
        """
        return get_user_stories(self, user_id)

    def get_user_reel(self, user_id):
        return get_user_reel(self, user_id)

    def get_self_story_viewers(self, story_id):
        return get_self_story_viewers(self, story_id)

    def get_pending_follow_requests(self):
        return get_pending_follow_requests(self)

    def get_your_medias(self, as_dict=False):
        """
        Returns your media ids. With parameter as_dict=True returns media as dict.
        :type as_dict: bool
        """
        return get_your_medias(self, as_dict)

    def get_archived_medias(self, as_dict=False):
        """
        Returns your archived media ids. With parameter as_dict=True returns media as dict.
        :type as_dict: bool
        """
        return get_archived_medias(self, as_dict)

    def get_timeline_medias(self):
        return get_timeline_medias(self)

    def get_popular_medias(self):
        return get_popular_medias(self)

    def get_user_medias(self, user_id, filtration=True, is_comment=False):
        return get_user_medias(self, user_id, filtration, is_comment)

    def get_total_user_medias(self, user_id):
        return get_total_user_medias(self, user_id)

    def get_last_user_medias(self, user_id, count):
        """
        Returns the last number of posts specified in count in media ids array.
        :type count: int
        :param count: Count of posts
        :return: array
        """
        return get_last_user_medias(self, user_id, count)

    def get_hashtag_medias(self, hashtag, filtration=True):
        return get_hashtag_medias(self, hashtag, filtration)

    def get_total_hashtag_medias(self, hashtag, amount=100, filtration=False):
        return get_total_hashtag_medias(self, hashtag, amount, filtration)

    def get_geotag_medias(self, geotag, filtration=True):
        return get_geotag_medias(self, geotag, filtration)

    def get_locations_from_coordinates(self, latitude, longitude):
        return get_locations_from_coordinates(self, latitude, longitude)

    def get_media_info(self, media_id):
        return get_media_info(self, media_id)

    def get_timeline_users(self):
        return get_timeline_users(self)

    def get_hashtag_users(self, hashtag):
        return get_hashtag_users(self, hashtag)

    def get_geotag_users(self, geotag):
        return get_geotag_users(self, geotag)

    def get_user_id_from_username(self, username):
        return get_user_id_from_username(self, username)

    def get_user_tags_medias(self, user_id):
        return get_user_tags_medias(self, user_id)

    def get_username_from_user_id(self, user_id):
        return get_username_from_user_id(self, user_id)

    def get_user_info(self, user_id, use_cache=True):
        return get_user_info(self, user_id, use_cache)

    def get_user_followers(self, user_id, nfollows=None):
        return get_user_followers(self, user_id, nfollows)

    def get_user_following(self, user_id, nfollows=None):
        return get_user_following(self, user_id, nfollows)

    def get_comment_likers(self, comment_id):
        return get_comment_likers(self, comment_id)

    def get_media_likers(self, media_id):
        return get_media_likers(self, media_id)

    def get_media_comments(self, media_id, only_text=False):
        return get_media_comments(self, media_id, only_text)

    def get_media_comments_all(self, media_id, only_text=False, count=False):
        return get_media_comments_all(self, media_id, only_text, count)

    def get_comment(self):
        return get_comment(self)

    def get_media_commenters(self, media_id):
        return get_media_commenters(self, media_id)

    def get_media_owner(self, media):
        return get_media_owner(self, media)

    def get_user_likers(self, user_id, media_count=10):
        return get_user_likers(self, user_id, media_count)

    def get_media_id_from_link(self, link):
        return get_media_id_from_link(self, link)

    def get_link_from_media_id(self, link):
        return get_link_from_media_id(self, link)

    def get_messages(self):
        return get_messages(self)

    def search_users(self, query):
        return search_users(self, query)

    def convert_to_user_id(self, usernames):
        return convert_to_user_id(self, usernames)

    def get_pending_thread_requests(self):
        return get_pending_thread_requests(self)

    # like

    def like(self, media_id, check_media=True):
        return like(self, media_id, check_media)

    def like_comment(self, comment_id):
        return like_comment(self, comment_id)

    def like_medias(self, media_ids, check_media=True):
        return like_medias(self, media_ids, check_media)

    def like_timeline(self, amount=None):
        return like_timeline(self, amount)

    def like_media_comments(self, media_id):
        return like_media_comments(self, media_id)

    def like_user(self, user_id, amount=None, filtration=True):
        return like_user(self, user_id, amount, filtration)

    def like_hashtag(self, hashtag, amount=None):
        return like_hashtag(self, hashtag, amount)

    def like_geotag(self, geotag, amount=None):
        return like_geotag(self, geotag, amount)

    def like_users(self, user_ids, nlikes=None, filtration=True):
        return like_users(self, user_ids, nlikes, filtration)

    def like_location_feed(self, place, amount):
        return like_location_feed(self, place, amount)

    def like_followers(self, user_id, nlikes=None, nfollows=None):
        return like_followers(self, user_id, nlikes, nfollows)

    def like_following(self, user_id, nlikes=None, nfollows=None):
        return like_following(self, user_id, nlikes, nfollows)

    # unlike

    def unlike(self, media_id):
        return unlike(self, media_id)

    def unlike_comment(self, comment_id):
        return unlike_comment(self, comment_id)

    def unlike_media_comments(self, media_id):
        return unlike_media_comments(self, media_id)

    def unlike_medias(self, media_ids):
        return unlike_medias(self, media_ids)

    def unlike_user(self, user):
        return unlike_user(self, user)

    # story
    def download_stories(self, username):
        return download_stories(self, username)

    def upload_story_photo(self, photo, upload_id=None):
        return upload_story_photo(self, photo, upload_id)

    # photo
    def download_photo(self, media_id, folder='photos', filename=None, save_description=False):
        return download_photo(self, media_id, folder, filename, save_description)

    def download_photos(self, medias, folder='photos', save_description=False):
        return download_photos(self, medias, folder, save_description)

    def upload_photo(self, photo, caption=None, upload_id=None, from_video=False):
        return upload_photo(self, photo, caption, upload_id, from_video)

    # video

    def upload_video(self, video, caption=''):
        return upload_video(self, video, caption)

    def download_video(self, media_id, folder='videos', filename=None, save_description=False):
        return download_video(self, media_id, folder, filename, save_description)

    # follow

    def follow(self, user_id):
        return follow(self, user_id)

    def follow_users(self, user_ids):
        return follow_users(self, user_ids)

    def follow_followers(self, user_id, nfollows=None):
        return follow_followers(self, user_id, nfollows)

    def follow_following(self, user_id, nfollows=None):
        return follow_following(self, user_id, nfollows)

    # unfollow

    def unfollow(self, user_id):
        return unfollow(self, user_id)

    def unfollow_users(self, user_ids):
        return unfollow_users(self, user_ids)

    def unfollow_non_followers(self, n_to_unfollows=None):
        return unfollow_non_followers(self, n_to_unfollows)

    def unfollow_everyone(self):
        return unfollow_everyone(self)

    def approve_pending_follow_requests(self):
        return approve_pending_follow_requests(self)

    def reject_pending_follow_requests(self):
        return reject_pending_follow_requests(self)

    # direct

    def send_message(self, text, user_ids, thread_id=None):
        return send_message(self, text, user_ids, thread_id)

    def send_messages(self, text, user_ids):
        return send_messages(self, text, user_ids)

    def send_media(self, media_id, user_ids, text=None, thread_id=None):
        return send_media(self, media_id, user_ids, text, thread_id)

    def send_medias(self, media_id, user_ids, text=None):
        return send_medias(self, media_id, user_ids, text)

    def send_hashtag(self, hashtag, user_ids, text='', thread_id=None):
        return send_hashtag(self, hashtag, user_ids, text, thread_id)

    def send_profile(self, profile_user_id, user_ids, text='', thread_id=None):
        return send_profile(self, profile_user_id, user_ids, text, thread_id)

    def send_like(self, user_ids, thread_id=None):
        return send_like(self, user_ids, thread_id)

    def approve_pending_thread_requests(self):
        return approve_pending_thread_requests(self)

    # delete

    def delete_media(self, media_id):
        return delete_media(self, media_id)

    def delete_medias(self, medias):
        return delete_medias(self, medias)

    def delete_comment(self, media_id, comment_id):
        return delete_comment(self, media_id, comment_id)

    # archive

    def archive(self, media_id, undo=False):
        return archive(self, media_id, undo)

    def unarchive(self, media_id):
        return archive(self, media_id, True)

    def archive_medias(self, medias):
        return archive_medias(self, medias)

    def unarchive_medias(self, medias):
        return unarchive_medias(self, medias)

    # comment

    def comment(self, media_id, comment_text):
        return comment(self, media_id, comment_text)

    def reply_to_comment(self, media_id, comment_text, parent_comment_id):
        return reply_to_comment(self, media_id, comment_text, parent_comment_id)

    def comment_hashtag(self, hashtag, amount=None):
        return comment_hashtag(self, hashtag, amount)

    def comment_medias(self, medias):
        return comment_medias(self, medias)

    def comment_user(self, user_id, amount=None):
        return comment_user(self, user_id, amount)

    def comment_users(self, user_ids, ncomments=None):
        return comment_users(self, user_ids, ncomments)

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

    def block_bots(self):
        return block_bots(self)

    # filter

    def filter_medias(self, media_items, filtration=True, quiet=False, is_comment=False):
        return filter_medias(self, media_items, filtration, quiet, is_comment)

    def check_media(self, media):
        return check_media(self, media)

    def check_user(self, user, unfollowing=False):
        return check_user(self, user, unfollowing)

    def check_not_bot(self, user):
        return check_not_bot(self, user)

    # support

    def check_if_file_exists(self, file_path, quiet=False):
        return check_if_file_exists(file_path, quiet)

    def extract_urls(self, text):
        return extract_urls(text)

    def read_list_from_file(self, file_path):
        return read_list_from_file(file_path)

    def console_print(self, text, color=None):
        return console_print(self, text, color)

    # stats

    def save_user_stats(self, username, path=""):
        return save_user_stats(self, username, path=path)
