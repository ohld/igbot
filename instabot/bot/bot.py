import os
import sys
import datetime
import atexit
import signal
import logging
import io
import collections
import datetime
import functools
import time

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
from .bot_get import get_user_info
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

from .bot_stats import save_user_stats

class Bot(API):
    def __init__(self,
                 whitelist=False,
                 blacklist=False,
                 comments_file=False,
                 max_likes_per_day=1000,
                 max_follows_per_day=350,
                 max_unfollows_per_day=350,
                 max_comments_per_day=100,
                 max_likes_to_like=100,
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
        self.max_likes_to_like = max_likes_to_like

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

    def get_user_info(self, user_id):
        return get_user_info(self, user_id)

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

# stats

    def save_user_stats(self, username):
        return save_user_stats(self, username)

# scheduler

class CancelJob(object):
    pass


class Scheduler(object):
    def __init__(self):
        self.jobs = []

    def run_pending(self):
        runnable_jobs = (job for job in self.jobs if job.should_run)
        for job in sorted(runnable_jobs):
            self._run_job(job)

    def run_all(self, delay_seconds=0):
        logger.info('Running *all* %i jobs with %is delay inbetween',
                    len(self.jobs), delay_seconds)
        for job in self.jobs[:]:
            self._run_job(job)
            time.sleep(delay_seconds)

    def clear(self, tag=None):
        if tag is None:
            del self.jobs[:]
        else:
            self.jobs[:] = (job for job in self.jobs if tag not in job.tags)

    def cancel_job(self, job):
        try:
            self.jobs.remove(job)
        except ValueError:
            pass

    def every(self, interval=1):
        job = Job(interval)
        self.jobs.append(job)
        return job

    def _run_job(self, job):
        ret = job.run()
        if isinstance(ret, CancelJob) or ret is CancelJob:
            self.cancel_job(job)

    @property
    def next_run(self):
        if not self.jobs:
            return None
        return min(self.jobs).next_run

    @property
    def idle_seconds(self):
        return (self.next_run - datetime.datetime.now()).total_seconds()


class Job(object):
    def __init__(self, interval):
        self.interval = interval  # pause interval * unit between runs
        self.job_func = None  # the job job_func to run
        self.unit = None  # time units, e.g. 'minutes', 'hours', ...
        self.at_time = None  # optional time at which this job runs
        self.last_run = None  # datetime of the last run
        self.next_run = None  # datetime of the next run
        self.period = None  # timedelta between runs, only valid for
        self.start_day = None  # Specific day of the week to start on
        self.tags = set()  # unique set of tags for the job

    def __lt__(self, other):
        return self.next_run < other.next_run

    def __repr__(self):
        def format_time(t):
            return t.strftime('%Y-%m-%d %H:%M:%S') if t else '[never]'

        timestats = '(last run: %s, next run: %s)' % (
                    format_time(self.last_run), format_time(self.next_run))

        if hasattr(self.job_func, '__name__'):
            job_func_name = self.job_func.__name__
        else:
            job_func_name = repr(self.job_func)
        args = [repr(x) for x in self.job_func.args]
        kwargs = ['%s=%s' % (k, repr(v))
                  for k, v in self.job_func.keywords.items()]
        call_repr = job_func_name + '(' + ', '.join(args + kwargs) + ')'

        if self.at_time is not None:
            return 'Every %s %s at %s do %s %s' % (
                   self.interval,
                   self.unit[:-1] if self.interval == 1 else self.unit,
                   self.at_time, call_repr, timestats)
        else:
            return 'Every %s %s do %s %s' % (
                   self.interval,
                   self.unit[:-1] if self.interval == 1 else self.unit,
                   call_repr, timestats)

    @property
    def second(self):
        assert self.interval == 1, 'Use seconds instead of second'
        return self.seconds

    @property
    def seconds(self):
        self.unit = 'seconds'
        return self

    @property
    def minute(self):
        assert self.interval == 1, 'Use minutes instead of minute'
        return self.minutes

    @property
    def minutes(self):
        self.unit = 'minutes'
        return self

    @property
    def hour(self):
        assert self.interval == 1, 'Use hours instead of hour'
        return self.hours

    @property
    def hours(self):
        self.unit = 'hours'
        return self

    @property
    def day(self):
        assert self.interval == 1, 'Use days instead of day'
        return self.days

    @property
    def days(self):
        self.unit = 'days'
        return self

    @property
    def week(self):
        assert self.interval == 1, 'Use weeks instead of week'
        return self.weeks

    @property
    def weeks(self):
        self.unit = 'weeks'
        return self

    @property
    def monday(self):
        assert self.interval == 1, 'Use mondays instead of monday'
        self.start_day = 'monday'
        return self.weeks

    @property
    def tuesday(self):
        assert self.interval == 1, 'Use tuesdays instead of tuesday'
        self.start_day = 'tuesday'
        return self.weeks

    @property
    def wednesday(self):
        assert self.interval == 1, 'Use wedesdays instead of wednesday'
        self.start_day = 'wednesday'
        return self.weeks

    @property
    def thursday(self):
        assert self.interval == 1, 'Use thursday instead of thursday'
        self.start_day = 'thursday'
        return self.weeks

    @property
    def friday(self):
        assert self.interval == 1, 'Use fridays instead of friday'
        self.start_day = 'friday'
        return self.weeks

    @property
    def saturday(self):
        assert self.interval == 1, 'Use saturdays instead of saturday'
        self.start_day = 'saturday'
        return self.weeks

    @property
    def sunday(self):
        assert self.interval == 1, 'Use sundays instead of sunday'
        self.start_day = 'sunday'
        return self.weeks

    def tag(self, *tags):
        if any([not isinstance(tag, collections.Hashable) for tag in tags]):
            raise TypeError('Every tag should be hashable')

        if not all(isinstance(tag, collections.Hashable) for tag in tags):
            raise TypeError('Tags must be hashable')
        self.tags.update(tags)
        return self

    def at(self, time_str):
        assert self.unit in ('days', 'hours') or self.start_day
        hour, minute = time_str.split(':')
        minute = int(minute)
        if self.unit == 'days' or self.start_day:
            hour = int(hour)
            assert 0 <= hour <= 23
        elif self.unit == 'hours':
            hour = 0
        assert 0 <= minute <= 59
        self.at_time = datetime.time(hour, minute)
        return self

    def do(self, job_func, *args, **kwargs):
        self.job_func = functools.partial(job_func, *args, **kwargs)
        try:
            functools.update_wrapper(self.job_func, job_func)
        except AttributeError:
            # job_funcs already wrapped by functools.partial won't have
            # __name__, __module__ or __doc__ and the update_wrapper()
            # call will fail.
            pass
        self._schedule_next_run()
        return self

    @property
    def should_run(self):
        return datetime.datetime.now() >= self.next_run

    def run(self):
        logger.info('Running job %s', self)
        ret = self.job_func()
        self.last_run = datetime.datetime.now()
        self._schedule_next_run()
        return ret

    def _schedule_next_run(self):
        assert self.unit in ('seconds', 'minutes', 'hours', 'days', 'weeks')
        self.period = datetime.timedelta(**{self.unit: self.interval})
        self.next_run = datetime.datetime.now() + self.period
        if self.start_day is not None:
            assert self.unit == 'weeks'
            weekdays = (
                'monday',
                'tuesday',
                'wednesday',
                'thursday',
                'friday',
                'saturday',
                'sunday'
            )
            assert self.start_day in weekdays
            weekday = weekdays.index(self.start_day)
            days_ahead = weekday - self.next_run.weekday()
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            self.next_run += datetime.timedelta(days_ahead) - self.period
        if self.at_time is not None:
            assert self.unit in ('days', 'hours') or self.start_day is not None
            kwargs = {
                'minute': self.at_time.minute,
                'second': self.at_time.second,
                'microsecond': 0
            }
            if self.unit == 'days' or self.start_day is not None:
                kwargs['hour'] = self.at_time.hour
            self.next_run = self.next_run.replace(**kwargs)
            # If we are running for the first time, make sure we run
            # at the specified time *today* (or *this hour*) as well
            if not self.last_run:
                now = datetime.datetime.now()
                if (self.unit == 'days' and self.at_time > now.time() and
                        self.interval == 1):
                    self.next_run = self.next_run - datetime.timedelta(days=1)
                elif self.unit == 'hours' and self.at_time.minute > now.minute:
                    self.next_run = self.next_run - datetime.timedelta(hours=1)
        if self.start_day is not None and self.at_time is not None:
            # Let's see if we will still make that time we specified today
            if (self.next_run - datetime.datetime.now()).days >= 7:
                self.next_run -= self.period


# The following methods are shortcuts for not having to
# create a Scheduler instance:

#: Default :class:`Scheduler <Scheduler>` object
default_scheduler = Scheduler()

#: Default :class:`Jobs <Job>` list
jobs = default_scheduler.jobs  # todo: should this be a copy, e.g. jobs()?


def every(interval=1):
    return default_scheduler.every(interval)


def run_pending():
    default_scheduler.run_pending()


def run_all(delay_seconds=0):
    default_scheduler.run_all(delay_seconds=delay_seconds)


def clear(tag=None):
    default_scheduler.clear(tag)


def cancel_job(job):
    default_scheduler.cancel_job(job)


def next_run():
    return default_scheduler.next_run


def idle_seconds():
    return default_scheduler.idle_seconds