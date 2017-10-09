import datetime
import atexit
import signal

from ..api import API

from .bot_archive import BotArchive
from .bot_block import BotBlock
from .bot_comment import BotComment
from .bot_delete import BotDelete
from .bot_direct import BotDirect
from .bot_filter import BotFilter
from .bot_follow import BotFollow
from .bot_get import BotGet
from .bot_like import BotLike
from .bot_photo import BotPhoto
from .bot_stats import BotStats
from .bot_support import BotSupport, check_if_file_exists, read_list_from_file
from .bot_unfollow import BotUnfollow
from .bot_unlike import BotUnlike
from .bot_video import BotVideo
from .bot_checkpoint import save_checkpoint, load_checkpoint


class Bot(API, BotArchive, BotBlock, BotComment, BotDelete,
          BotDirect, BotFilter, BotFollow, BotGet, BotLike,
          BotPhoto, BotStats, BotSupport, BotUnfollow, BotUnlike,
          BotVideo):

    def __init__(self,
                 whitelist=False,
                 blacklist=False,
                 comments_file=False,
                 proxy=None,
                 max_likes_per_day=1000,
                 max_unlikes_per_day=1000,
                 max_follows_per_day=350,
                 max_unfollows_per_day=350,
                 max_comments_per_day=100,
                 max_blocks_per_day=100,
                 max_unblocks_per_day=100,
                 max_likes_to_like=100,
                 filter_users=True,
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
                 stop_words=None):
        super(self.__class__, self).__init__()
        self.total_liked = 0
        self.total_unliked = 0
        self.total_followed = 0
        self.total_unfollowed = 0
        self.total_commented = 0
        self.total_blocked = 0
        self.total_unblocked = 0
        self.total_archived = 0
        self.total_unarchived = 0
        self.start_time = datetime.datetime.now()

        # the time.time() of the last action
        self.last_like = 0
        self.last_unlike = 0
        self.last_follow = 0
        self.last_unfollow = 0
        self.last_comment = 0
        self.last_block = 0
        self.last_unblock = 0

        # limits - follow
        self.filter_users = filter_users
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
        self.stop_words = stop_words or ['shop', 'store', 'free']

        # limits - block
        self.max_following_to_block = max_following_to_block

        # delays
        self.like_delay = like_delay
        self.unlike_delay = unlike_delay
        self.follow_delay = follow_delay
        self.unfollow_delay = unfollow_delay
        self.comment_delay = comment_delay
        self.block_delay = block_delay
        self.unblock_delay = unblock_delay

        # current following
        self.following = []

        # proxy
        self.proxy = proxy

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

        self.logger.info('Instabot Started')

    def version(self):
        try:
            from pip._vendor import pkg_resources
        except ImportError:
            import pkg_resources
        return next((p.version for p in pkg_resources.working_set if p.project_name.lower() == 'instabot'), "No match")

    def logout(self):
        save_checkpoint(self)
        super(Bot, self).logout()
        self.logger.info("Bot stopped. "
                         "Worked: %s" % (datetime.datetime.now() - self.start_time))
        self.print_counters()

    def login(self, **args):
        if self.proxy:
            args['proxy'] = self.proxy
        super(Bot, self).login(**args)
        self.prepare()
        signal.signal(signal.SIGTERM, self.logout)
        atexit.register(self.logout)

    def prepare(self):
        storage = load_checkpoint(self)
        if storage is not None:
            self.total_liked, self.total_unliked, self.total_followed, self.total_unfollowed, self.total_commented, self.total_blocked, self.total_unblocked, self.total_requests, self.start_time, self.total_archived, self.total_unarchived = storage
        if not self.whitelist:
            self.whitelist = self.check_whitelists()
        self.whitelist = list(
            filter(None, map(self.convert_to_user_id, self.whitelist)))
        self.blacklist = list(
            filter(None, map(self.convert_to_user_id, self.blacklist)))

    def print_counters(self):
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
        if self.total_archived:
            self.logger.info("Total archived: %d" % self.total_archived)
        if self.total_unarchived:
            self.logger.info("Total unarchived: %d" % self.total_unarchived)
        self.logger.info("Total requests: %d" % self.total_requests)

    # support

    def check_if_file_exists(self, file_path):
        return check_if_file_exists(file_path)

    def read_list_from_file(self, file_path):
        return read_list_from_file(file_path)
