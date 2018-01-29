import datetime
import atexit
import signal
import math
import os

from ..api import API
from ..api import api_db
from random import randint


from .bot_get import get_media_owner, get_your_medias, get_user_medias
from .bot_get import get_timeline_medias, get_hashtag_medias, get_user_info, get_location_medias
from .bot_get import get_geotag_medias, get_timeline_users, get_hashtag_users
from .bot_get import get_media_commenters, get_userid_from_username, get_username_from_userid
from .bot_get import crawl_other_user_followers, get_user_following, get_media_likers, get_popular_medias, \
    crawl_user_followers
from .bot_get import get_media_comments, get_geotag_users, get_locations_from_coordinates, convert_to_user_id
from .bot_get import get_comment, get_media_info, get_user_likers, get_archived_medias, get_total_user_medias

from .bot_like import like, like_medias, like_timeline, like_user, like_users, like_own_followers, \
    like_other_users_followers
from .bot_like import like_hashtag, like_geotag, like_followers, like_following, like_posts_by_location

from .bot_unlike import unlike, unlike_medias, unlike_user

from .bot_photo import download_photo, download_photos, upload_photo

from .bot_video import upload_video

from .bot_follow import follow, follow_users, follow_followers, follow_following, follow_users_by_location, \
    follow_users_by_hashtag, follow_other_users_followers

from .bot_unfollow import unfollow, unfollow_users, unfollow_non_followers, unfollowBotCreatedFollowings
from .bot_unfollow import unfollow_everyone, update_unfollow_file

from .bot_archive import archive, archive_medias, unarchive_medias

from .bot_comment import comment, comment_medias, comment_geotag, comment_users
from .bot_comment import comment_hashtag, is_commented, comment_user

from .bot_block import block, unblock, block_users, unblock_users, block_bots

from .bot_checkpoint import save_checkpoint, load_checkpoint

from .bot_filter import filter_medias, check_media, filter_users, check_user
from .bot_filter import check_not_bot

from .bot_support import check_if_file_exists, read_list_from_file, check_whitelists
from .bot_support import add_whitelist, add_blacklist

from .bot_stats import save_user_stats

from .bot_util import getBotOperations, get_follow_delay,get_like_delay
from .bot_action_handler import  getLikeAmount,getFollowAmount,getAmountDistribution, getLikesPerformed, getFollowPerformed

class Bot(API):
    def __init__(self,
                 id_campaign,
                 whitelist=False,
                 blacklist=False,
                 comments_file=False,
                 proxy=None,
                 multiple_ip=None,
                 is_bot_account =False,
                 max_likes_per_day=1000,
                 max_unlikes_per_day=1000,
                 max_follows_per_day=350,
                 max_unfollows_per_day=350,
                 max_comments_per_day=100,
                 max_blocks_per_day=100,
                 max_unblocks_per_day=100,
                 max_likes_to_like=500000,
                 filter_users=True,
                 max_followers_to_follow=2000,
                 min_followers_to_follow=10,
                 max_following_to_follow=2000,
                 min_following_to_follow=10,
                 max_followers_to_following_ratio=10,
                 max_following_to_followers_ratio=4,
                 min_media_count_to_follow=20,
                 max_following_to_block=2000,
                 like_delay=15,
                 like_delay_if_bot_blocked=40,
                 unlike_delay=10,
                 follow_delay=30,
                 unfollow_delay=30,
                 comment_delay=60,
                 block_delay=30,
                 unblock_delay=30,
                 stop_words=['sex', 'penis', 'fuck']):
        super(self.__class__, self).__init__()
        self.initLogging(id_campaign)

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
        self.stop_words = stop_words

        # limits - block
        self.max_following_to_block = max_following_to_block

        # delays
        self.like_delay = like_delay
        self.like_delay_if_bot_blocked = like_delay_if_bot_blocked
        self.unlike_delay = unlike_delay
        self.follow_delay = follow_delay
        self.unfollow_delay = unfollow_delay
        self.comment_delay = comment_delay
        self.block_delay = block_delay
        self.unblock_delay = unblock_delay

        # proxy
        self.proxy = proxy
        self.multiple_ip = multiple_ip
        self.is_bot_account = is_bot_account
        self.bot_ip = None

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

        #todo-> when starting the bot without a campaign(eg. searchByLocation) the below data is undefined and sometomes might cause issues
        #todo-> improve the functionality to have a separate handler for the actions that do not require an campaign
        
        self.id_campaign = id_campaign
        self.campaignObject = api_db.getCampaign(self.id_campaign)
        if self.campaignObject!=None:
          self.web_application_id_user = self.campaignObject['id_user']
        else:
          self.web_application_id_user=None
          

    def check_ip(self):
        print(self.session.get('http://bot.whatismyipaddress.com/').text)

    def version(self):
        try:
            from pip._vendor import pkg_resources
        except ImportError:
            import pkg_resources
        return next((p.version for p in pkg_resources.working_set if p.project_name.lower() == 'instabot'), "No match")

    def logout(self):

        #release ip
        self.logger.info("logout: Going to release the ip")
        api_db.insert("update campaign set id_ip_bot=null where id_campaign=%s",self.id_campaign)
        if self.id_campaign != False:
            save_checkpoint(self)

        super(self.__class__, self).logout()
        self.logger.info("logout: Bot stopped. "
                         "Worked: %s" % (datetime.datetime.now() - self.start_time))
        self.print_counters()

    def login(self, **args):
        if self.proxy:
            args['proxy'] = self.proxy
        status = super(self.__class__, self).login(**args)
        #if status==False:
        #    exit("Could not login to instagram !")
        self.prepare()
        signal.signal(signal.SIGTERM, self.logout)
        atexit.register(self.logout)
        return status

    def prepare(self):
        storage = load_checkpoint(self)
        if storage is not None:
            self.total_liked, self.total_unliked, self.total_followed, self.total_unfollowed, self.total_commented, self.total_blocked, self.total_unblocked, self.total_requests, self.start_time, self.total_archived, self.total_unarchived = storage

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

    # getters

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

    def get_timeline_medias(self, amount):
        return get_timeline_medias(self, amount=amount)

    def get_popular_medias(self):
        return get_popular_medias(self)

    def get_user_medias(self, user_id, filtration=True, is_comment=False):
        return get_user_medias(self, user_id, filtration, is_comment)

    def get_total_user_medias(self, user_id):
        return get_total_user_medias(self, user_id)

    def get_location_medias(self, id_location, filtration=True, amount=None):
        return get_location_medias(self, id_location, filtration, amount)

    def get_hashtag_medias(self, hashtag, filtration=True, amount=50):
        return get_hashtag_medias(self, hashtag, filtration, amount)

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

    def get_userid_from_username(self, username):
        return get_userid_from_username(self, username)

    def get_username_from_userid(self, userid):
        return get_username_from_userid(self, userid)

    def get_user_info(self, user_id):
        return get_user_info(self, user_id)

    def crawl_other_user_followers(self, userObject, amount=None):
        return crawl_other_user_followers(self, userObject, amount)

    def crawl_user_followers(self, amount=1500):
        return crawl_user_followers(self, amount)

    def get_user_following(self, user_id, nfollows=None):
        return get_user_following(self, user_id, nfollows)

    def get_media_likers(self, media_id):
        return get_media_likers(self, media_id)

    def get_media_comments(self, media_id, only_text=False):
        return get_media_comments(self, media_id, only_text)

    def get_comment(self):
        return get_comment(self)

    def get_media_commenters(self, media_id):
        return get_media_commenters(self, media_id)

    def get_media_owner(self, media):
        return get_media_owner(self, media)

    def get_user_likers(self, user_id, media_count=10):
        return get_user_likers(self, user_id, media_count)

    def convert_to_user_id(self, usernames):
        return convert_to_user_id(self, usernames)

    # like

    def like(self, media_id):
        return like(self, media_id)

    def like_medias(self, medias, bot_operation, bot_operation_value=None):
        return like_medias(self, medias, bot_operation, bot_operation_value)

    def like_timeline(self, amount=None):
        return like_timeline(self, amount=amount)

    def like_user(self, userObject, bot_operation, bot_operation_value=None, amount=2, filtration=True):
        return like_user(self, userObject=userObject, bot_operation=bot_operation,
                         bot_operation_value=bot_operation_value, amount=amount, filtration=filtration)

    def like_hashtag(self, hashtag, amount=None):
        return like_hashtag(self, hashtag, amount)

    def like_posts_by_location(self, locationObject, amount):
        return like_posts_by_location(self, locationObject, amount)

    def like_geotag(self, geotag, amount=None):
        return like_geotag(self, geotag, amount)

    def like_users(self, user_ids, nlikes=None, filtration=True):
        return like_users(self, user_ids, nlikes, filtration)

    def like_own_followers(self, amount):
        return like_own_followers(self, likesAmount=amount)

    def like_other_users_followers(self, userObject, amount):
        return like_other_users_followers(self, userObject=userObject, amount=amount)

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

    # photo

    def download_photo(self, media_id, path='photos/', filename=None, description=False):
        return download_photo(self, media_id, path, filename, description)

    def download_photos(self, medias, path='photos/', description=False):
        return download_photos(self, medias, path, description)

    def upload_photo(self, photo, caption=None, upload_id=None):
        return upload_photo(self, photo, caption, upload_id)

    # video

    def upload_video(self, video, thumbnail, caption=''):
        return upload_video(self, video, thumbnail, caption)

    # follow

    def follow(self, user_id):
        return follow(self, user_id)

    def follow_users(self, users, amount, bot_operation, bo_operation_value):
        return follow_users(self, users, amount, bot_operation, bo_operation_value)

    def follow_followers(self, user_id, nfollows=None):
        return follow_followers(self, user_id, nfollows)

    def follow_following(self, user_id):
        return follow_following(self, user_id)

    def follow_users_by_location(self, locationObject, amount):
        return follow_users_by_location(self, locationObject=locationObject, amount=amount)

    def follow_users_by_hashtag(self, hashtag, amount):
        return follow_users_by_hashtag(self, hashtag=hashtag, amount=amount)

    def follow_other_users_followers(self, userObject, amount):
        return follow_other_users_followers(self, userObject, amount)

    # unfollow

    def unfollow(self, user_id):
        return unfollow(self, user_id)

    def unfollowBotCreatedFollowings(self, amount):
        return unfollowBotCreatedFollowings(self, amount)

    def unfollow_users(self, user_ids):
        return unfollow_users(self, user_ids)

    def unfollow_non_followers(self, n_to_unfollows=None):
        return unfollow_non_followers(self, n_to_unfollows)

    def unfollow_everyone(self):
        return unfollow_everyone(self)

    def update_unfollow_file(self):
        return update_unfollow_file(self)

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

    def comment_hashtag(self, hashtag):
        return comment_hashtag(self, hashtag)

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

    def check_user(self, user, filter_closed_acc=False):
        return check_user(self, user, filter_closed_acc)

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

    def save_user_stats(self, username, path=""):
        return save_user_stats(self, username, path=path)

    def get_follow_delay(self, followAmount):
        return get_follow_delay(self, followAmount)

    def get_like_delay(self, likeAmount):
        return get_like_delay(self, likeAmount)

    def getBotOperations(self, id_campaign):
        return getBotOperations(self, id_campaign)
      
    def getLikeAmount(self, id_campaign,calculatedAmount):
        return getLikeAmount(self, id_campaign,calculatedAmount)
      
    def getFollowAmount(self, id_campaign,calculatedAmount):
      return getFollowAmount(self, id_campaign,calculatedAmount)
    
    def getLikesPerformed(self, dateParam):
      return getLikesPerformed(self, dateParam)
    
    def getFollowPerformed(self, dateParam):
      return getFollowPerformed(self, dateParam)
    
    def getAmountDistribution(self,id_campaign):
      return getAmountDistribution(self,id_campaign)

    #this function check if another bot instance for same campaign is running
    def canBotStart(self, id_campaign):
        self.logger.info("canBotStart: check if another bot instance is running for campaign %s",id_campaign)
        processname = 'angie_idc'+id_campaign+' '
        tmp = os.popen("ps -Af").read()
        proccount = tmp.count(processname)

        if proccount > 1:
            self.logger.info("canBotStart: ERROR: another bot instance is running for campaign %s", id_campaign)
            exit("canBotStart: ERROR: another bot instance is running for this campaign")

        self.logger.info("canBotStart: All Good, no other bot instance is running for this campaign")
        return True


    def getUsersForLikeForLike(self, id_campaign,likesAmount):
      
      sqlLastUserProcessed = "SELECT * FROM `campaign_checkpoint` WHERE   date(timestamp) = CURDATE() and id_campaign=%s and _key='like_for_like_user_id'"
      lastUserProcessed = api_db.fetchOne(sqlLastUserProcessed,id_campaign)
      
      
      #start from beginning
      if not lastUserProcessed:
        lastUserProcessedId = 0
      else:
        lastUserProcessedId = lastUserProcessed['value']
        
      self.logger.info("getAmountLikeForLike: Last user processed is: %s ",lastUserProcessedId)
      
      usersToProcess = "select DISTINCT users.email,users.id_user, campaign.username as instagram_username from users join user_subscription on (users.id_user = user_subscription.id_user)  join campaign on (users.id_user = campaign.id_user) where (user_subscription.end_date>now() or user_subscription.end_date is null) and users.id_user>%s  and campaign.id_campaign!=%s order by users.id_user asc limit %s"
      
      result = api_db.select(usersToProcess,lastUserProcessedId,id_campaign,likesAmount)
      
      self.logger.info("getAmountLikeForLike: Found: users: %s", len(result))
      
      return result
      
      
    def startLikeForLike(self, likesAmount):
      self.logger.info("bot.startLikeForLike: Started likeForLike operation. Likes to perform %s", likesAmount)
      totalLiked=0
      
      result=self.getUsersForLikeForLike(self.id_campaign,likesAmount)
      
      self.logger.info("bot.startLikeForLike: Received %s users to process", len(result))
      
      if len(result)==0:
        self.logger.info("bot.startLikeForLike. NOTHING TO LIKE")
        return 0
      
      for user in result:
        user['instagram_id_user']=self.get_userid_from_username(user['instagram_username'])
        user['full_name']=user['instagram_username']
        totalLiked = totalLiked + self.like_user(userObject=user, bot_operation="like_for_like", bot_operation_value=user['instagram_username'],amount=1)
        #update in database the user id
        api_db.updateCampaignChekpoint('like_for_like_user_id',user['id_user'],self.id_campaign)
        
        
      self.logger.info("bot.startLikeForLike: END. Last user processed: %s, id_user: %s" % (user['instagram_username'], user['id_user']))
      
      self.logger.info("bot.startLikeForLike: END updated checkpoint for campaign: %s with last user: %s" % (self.id_campaign, user['id_user']))
      self.logger.info("bot.startLikeForLike: END. Total liked %s users from a total of %s users" % (totalLiked, likesAmount))
      
      return totalLiked
      
    def startStandardOperation(self, likesAmount, followAmount, operations):

        result = {}
        result['no_likes'] = 0
        result['no_follows'] = 0

        self.logger.info("bot.startStandardOperation: Started standard operation. Likes to perform: %s, follow to perform %s, operations %s!" % (likesAmount, followAmount, len(operations)))

        for operation in operations:
            self.currentOperation=operation['configName']

            if 'like_own_followers' == operation['configName']:
                if likesAmount < 1:
                    self.logger.info("like_own_followers: Likes to perform 0, going to skip !")
                    continue

                expectedLikes = int(math.ceil(math.ceil(operation['percentageAmount'] * likesAmount) / math.ceil(100)))

                self.logger.info(
                    "like_own_followers: Start bot operation: %s, percentage: %s , totalAmountOfLikes: %s, totalToPerformAfterPecerntageApplied: %s" % (
                        'like_own_followers', operation['percentageAmount'], likesAmount, expectedLikes))
                performedLikes = self.like_own_followers(expectedLikes)

                self.logger.info("like_own_followers: End operation: %s, expected: %s, performed: %s" % (
                    'like_own_followers', expectedLikes, performedLikes))

                result['no_likes'] = result['no_likes'] + performedLikes

            if 'like_timeline' == operation['configName']:
                # maybe this check can be set globally for all likes operation type
                if likesAmount < 1:
                    self.logger.info("like_timeline:Likes to perform 0, going to skip !")
                    continue

                expectedLikes = int(math.ceil(math.ceil(operation['percentageAmount'] * likesAmount) / math.ceil(100)))

                self.logger.info(
                    "like_timeline: Start bot operation: %s, percentage: %s , totalAmountOfLikes: %s, totalToPerformAfterPecerntageApplied: %s" % (
                        'like_timeline', operation['percentageAmount'], likesAmount, expectedLikes))
                performedLikes = self.like_timeline(expectedLikes)

                self.logger.info(
                    "like_timeline: End operation: %s, expected: %s, performed: %s" % ('like_timeline', expectedLikes, performedLikes))

                result['no_likes'] = result['no_likes'] + performedLikes

            if 'like_posts_by_hashtag' == operation['configName']:
                if likesAmount < 1:
                    self.logger.info("like_posts_by_hashtag: Likes to perform 0, going to skip !")
                    continue
                performedLikes = 0
                expectedLikes = int(math.ceil(math.ceil(operation['percentageAmount'] * likesAmount) / math.ceil(100)))

                iteration = 0
                securityBreak = 40

                self.logger.info(
                    "like_posts_by_hashtag: Start bot operation: %s, percentage: %s , totalAmountOfLikes: %s, totalToPerformAfterPecerntageApplied: %s" % (
                        'like_posts_by_hashtag', operation['percentageAmount'], likesAmount,
                        expectedLikes))

                while iteration < securityBreak and performedLikes< expectedLikes:
                    if len(operation['list']) == 0:
                        self.logger.info(
                            "like_posts_by_hashtag: No hashtag left for operation like_posts_by_hashtag, skipping this operation...")
                        break

                    hashtagIndex = randint(0, len(operation['list']) - 1)
                    hashtagObject = operation['list'][hashtagIndex]

                    self.logger.info("like_posts_by_hashtag: Iteration: %s, hashtag: %s, amountToPerform %s, initialAmount: %s ", iteration,
                                     hashtagObject['hashtag'],expectedLikes - performedLikes,expectedLikes)
                    performedLikes += self.like_hashtag(hashtagObject['hashtag'],expectedLikes- performedLikes)

                    self.logger.info(
                        "like_posts_by_hashtag: End  iteration: %s, hashtag: %s, expected: %s, actual:%s",
                        iteration, hashtagObject['hashtag'],expectedLikes, performedLikes)
                    del operation['list'][hashtagIndex]
                    iteration += 1
                self.logger.info("like_posts_by_hashtag: End bot operation %s ", "like_posts_by_hashtag")

                result['no_likes'] = result['no_likes'] + performedLikes

            if 'like_other_users_followers' == operation['configName']:
                if likesAmount < 1:
                    self.logger.info("like_other_users_followers: Likes to perform 0, going to skip !")
                    continue
                performedLikes = 0
                expectedLikes = int(math.ceil(math.ceil(operation['percentageAmount'] * likesAmount) / math.ceil(100)))

                iteration = 0
                securityBreak = 40

                self.logger.info(
                    "like_other_users_followers: Start bot operation: %s, percentage: %s , totalAmountOfLikes: %s, totalToPerformAfterPecerntageApplied: %s" % (
                        'like_other_users_followers', operation['percentageAmount'], likesAmount, expectedLikes))

                while iteration < securityBreak and performedLikes < expectedLikes:
                    if len(operation['list']) == 0:
                        self.logger.info(
                            "like_other_users_followers: No users left for operation like_other_users_followers, skipping this operation...")
                        break

                    index = randint(0, len(operation['list']) - 1)
                    userObject = operation['list'][index]

                    self.logger.info(
                        "like_other_users_followers: Iteration: %s, user: %s, amountToPerform in this iteration:  %s, initialAmount: %s ",
                        iteration, userObject['username'], expectedLikes - performedLikes, expectedLikes)

                    performedLikes += self.like_other_users_followers(userObject, expectedLikes - performedLikes)

                    self.logger.info("%s: iteration: %s, user: %s, expected: %s, actual:%s",
                                     'like_other_users_followers', iteration, userObject['username'], expectedLikes,
                                     performedLikes)
                    del operation['list'][index]
                    iteration += 1
                self.logger.info("like_other_users_followers: End bot operation %s ")

                result['no_likes'] = result['no_likes'] + performedLikes

            if 'like_posts_by_location' == operation['configName']:
                if likesAmount < 1:
                    self.logger.info("like_posts_by_location: Likes to perform 0, going to skip !")
                    continue
                performedLikes = 0
                expectedLikes = int(math.ceil(math.ceil(operation['percentageAmount'] * likesAmount) / math.ceil(100)))

                iteration = 0
                securityBreak = 40

                self.logger.info(
                    "like_posts_by_location: Start bot operation: %s, percentage: %s , totalAmountOfLikes: %s, totalToPerformAfterPecerntageApplied: %s" % (
                        'like_posts_by_location', operation['percentageAmount'], likesAmount, expectedLikes))

                while iteration < securityBreak and performedLikes < expectedLikes:
                    if len(operation['list']) == 0:
                        self.logger.info(
                            "like_posts_by_location: No location left for operation like_posts_by_location, skipping this operation...")
                        break

                    locationIndex = randint(0, len(operation['list']) - 1)
                    locationObject = operation['list'][locationIndex]

                    self.logger.info(
                        "like_posts_by_location: Iteration: %s, location: %s, amountToPerform in this iteration:  %s, initialAmount: %s ",
                        iteration, locationObject['location'], expectedLikes - performedLikes, expectedLikes)

                    performedLikes += self.like_posts_by_location(locationObject, expectedLikes - performedLikes)

                    self.logger.info("%s: iteration: %s, location: %s, expected: %s, actual:%s",
                                     'LIKE_POSTS_BY_LOCATION', iteration, locationObject['location'], expectedLikes,
                                     performedLikes)
                    del operation['list'][locationIndex]
                    iteration += 1
                self.logger.info("like_posts_by_location: End bot operation %s ", "like_posts_by_location")

                result['no_likes'] = result['no_likes'] + performedLikes

            if 'follow_users_by_hashtag' == operation['configName']:
                if followAmount < 1:
                    self.logger.info("Follows to perform 0, going to skip !")
                    continue
                performedFollow = 0
                expectedFollow = int(math.ceil(math.ceil(operation['percentageAmount'] * followAmount) / math.ceil(100)))

                iteration = 0
                securityBreak = 30

                self.logger.info(
                    "follow_users_by_hashtag: Start bot operation: %s, percentage: %s , totalFollowToPerform: %s, totalToPerformAfterPecerntageApplied: %s" % (
                        'follow_users_by_hashtag', operation['percentageAmount'], followAmount, expectedFollow))

                while iteration < securityBreak and performedFollow < expectedFollow:
                    if len(operation['list']) == 0:
                        self.logger.info(
                            "follow_users_by_hashtag: No hashtags left for operation follow_users_by_hashtag, skipping this operation...")
                        break

                    index = randint(0, len(operation['list']) - 1)
                    hashtagObject = operation['list'][index]

                    self.logger.info(
                        "follow_users_by_hashtag: Iteration: %s, hashtag: %s, amountToPerform in this iteration:  %s, initialAmount: %s ",
                        iteration, hashtagObject['hashtag'], expectedFollow - performedFollow, expectedFollow)

                    performedFollow += self.follow_users_by_hashtag(hashtag=hashtagObject['hashtag'],
                                                                    amount=expectedFollow - performedFollow)

                    self.logger.info("%s: iteration: %s, hashtag: %s, expected: %s, actual:%s",
                                     'follow_users_by_hashtag', iteration, hashtagObject['hashtag'], expectedFollow,
                                     performedFollow)
                    del operation['list'][index]
                    iteration += 1
                self.logger.info("follow_users_by_hashtag: End bot operation %s ", "follow_users_by_hashtag")

                result['no_follows'] =result['no_follows'] + performedFollow

            if 'follow_users_by_location' == operation['configName']:
                if followAmount < 1:
                    self.logger.info("follow_users_by_location: Follows to perform 0, going to skip !")
                    continue

                performedFollow = 0
                expectedFollow = int(math.ceil(math.ceil(operation['percentageAmount'] * followAmount) / math.ceil(100)))

                iteration = 0
                securityBreak = 30

                self.logger.info(
                    "follow_users_by_location: Start bot operation: %s, percentage: %s , totalFollowToPerform: %s, totalToPerformAfterPecerntageApplied: %s" % (
                        'follow_users_by_location', operation['percentageAmount'], followAmount, expectedFollow))

                while iteration < securityBreak and performedFollow < expectedFollow:
                    if len(operation['list']) == 0:
                        self.logger.info(
                            "follow_users_by_location: No location left for operation follow_users_by_location, skipping this operation...")
                        break

                    index = randint(0, len(operation['list']) - 1)
                    locationObject = operation['list'][index]

                    self.logger.info(
                        "follow_users_by_location: Iteration: %s, location: %s, amountToPerform in this iteration:  %s, initialAmount: %s ",
                        iteration, locationObject['location'], expectedFollow - performedFollow, expectedFollow)

                    performedFollow += self.follow_users_by_location(locationObject=locationObject,amount=expectedFollow - performedFollow)

                    self.logger.info("%s: iteration: %s, location: %s, expected: %s, actual:%s",
                                     'follow_users_by_location', iteration, locationObject['location'], expectedFollow,
                                     performedFollow)
                    del operation['list'][index]
                    iteration += 1
                self.logger.info("follow_users_by_location: End bot operation %s ", "follow_users_by_location")

                result['no_follows'] = result['no_follows'] + performedFollow

            if 'follow_other_users_followers' == operation['configName']:
                if followAmount < 1:
                    self.logger.info("follow_other_users_followers: Follows to perform 0, going to skip !")
                    continue

                performedFollow = 0
                expectedFollow = int(
                    math.ceil(math.ceil(operation['percentageAmount'] * followAmount) / math.ceil(100)))

                iteration = 0
                securityBreak = 30

                self.logger.info(
                    "follow_other_users_followers: Start bot operation: %s, percentage: %s , totalFollowToPerform: %s, totalToPerformAfterPecerntageApplied: %s" % (
                        'follow_other_users_followers', operation['percentageAmount'], followAmount, expectedFollow))

                while iteration < securityBreak and performedFollow < expectedFollow:
                    if len(operation['list']) == 0:
                        self.logger.info(
                            "follow_other_users_followers: No users left for operation follow_other_users_followers, skipping this operation...")
                        break

                    index = randint(0, len(operation['list']) - 1)
                    userObject = operation['list'][index]

                    self.logger.info(
                        "follow_other_users_followers: Iteration: %s, user: %s, amountToPerform in this iteration:  %s, initialAmount: %s ",
                        iteration, userObject['username'], expectedFollow - performedFollow, expectedFollow)

                    performedFollow += self.follow_other_users_followers(userObject=userObject, amount=expectedFollow-performedFollow)

                    self.logger.info("%s: iteration: %s, user: %s, expected: %s, actual:%s",
                                     'follow_other_users_followers', iteration, userObject['username'], expectedFollow,
                                     performedFollow)
                    del operation['list'][index]
                    iteration += 1
                self.logger.info("follow_other_users_followers: End bot operation %s ", "follow_other_users_followers")

                result['no_follows'] = result['no_follows'] + performedFollow

            if 'unfollow' == operation['configName']:

                if followAmount < 1:
                    self.logger.info("unfollow: Unfollow to perform 0, going to skip !")
                    continue

                expectedFollow = int(math.ceil(math.ceil(operation['percentageAmount'] * followAmount) / math.ceil(100)))

                self.logger.info(
                    "unfollow: Start bot operation: %s, percentage: %s , totalUNFOLLOWToPerform: %s, totalToPerformAfterPecerntageApplied: %s" % (
                        'unfollow', operation['percentageAmount'], followAmount, expectedFollow))
                performedFollow = self.unfollowBotCreatedFollowings(amount=expectedFollow)

                self.logger.info("unfollow: End operation: %s, expected: %s, actual: %s" % ('unfollow', expectedFollow, performedFollow))

                result['no_follows'] = result['no_follows'] + performedFollow
        
        self.logger.info("bot.startStandardOperation. END operation. performed likes %s, follow/unfollow %s . Expected like %s, follow %s" % (result['no_likes'],result['no_follows'], likesAmount, followAmount))
        return result
