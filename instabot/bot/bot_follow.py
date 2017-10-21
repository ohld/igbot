from tqdm import tqdm

from . import limits
from . import delay
from ..api import api_db
from random import randint
import time


def follow(self, user):
    self.logger.info('Going to Follow user: %s ' % user['username'])

    delay.follow_delay(self)
    if super(self.__class__, self).follow(user['instagram_id_user']):
        self.logger.info("Successfully followed user %s " % user['username'])
        self.total_followed += 1
        return True

    return False


#todo add check user
def follow_users_by_location(self, locationObject, amount):
    self.logger.info("Going to follow %s users from location %s." % (amount, locationObject['location']))

    medias = self.getLocationFeed(locationObject['id_location'],amount)

    users = []

    for media in medias:
        user = media['user']
        user['media'] = {}
        user['instagram_id_user']=user['pk']
        user['media']['code'] = media['code']
        user['media']['image'] = media['image_versions2']['candidates'][0]['url']
        user['media']['id'] = media['pk']
        users.append(user)

    bot_operation = 'follow_users_by_location'
    return self.follow_users(users[:amount], bot_operation, locationObject['location'])

#todo add check user
def follow_users_by_hashtag(self,hashtag,amount):
    feed = self.getHashtagFeed(hashtag, amount)
    users = []

    for media in feed:
        user = media['user']
        user['media'] = {}
        user['instagram_id_user'] = user['pk']
        user['media']['code'] = media['code']
        user['media']['image'] = media['image_versions2']['candidates'][0]['url']
        user['media']['id'] = media['pk']
        users.append(user)
    bot_operation = 'follow_users_by_hashtag'

    return self.follow_users(users[:amount], bot_operation, hashtag)

def follow_other_users_followers(self,userObject,amount):
    self.logger.info('Going to follow %s followers of user: %s' % (amount, userObject['username']))

    self.crawl_other_user_followers(userObject=userObject, amount=500)
    
    totalFollowersResult = api_db.fetchOne("select count(*) as total_followers from instagram_user_followers  where fk=%s order by id asc", userObject['id'])

    self.logger.info('Total followers in  database: %s', totalFollowersResult['total_followers'])
    
    batchSize=amount*3

    self.logger.info('Getting followers from DATABASE limit %s' % ( batchSize))
    query="select iuf.*, id_campaign from instagram_user_followers iuf " \
    "join instagram_users on (iuf.fk=instagram_users.id) " \
    "join campaign_config on (instagram_users.id_config=campaign_config.id_config) " \
    "where instagram_users.username=%s " \
    "and iuf.username not in  " \
    "(select username from bot_action where id_campaign=campaign_config.id_campaign and bot_operation like %s) limit %s"
    
    followers = api_db.select(query, userObject['username'], 'follow' + '%', batchSize)

    self.logger.info('Received from database %s followers', len(followers))
    
    users = []

    iteration = 0
    securityBreak = 0
    filteredFollowers=[]
    
    
    # check if this follower is valid -> this might not be required / usefull as it takes alot of time to perform the check
    self.logger.info("Going to check users")

    while len(filteredFollowers) < amount and securityBreak < 400 and len(followers)>iteration+1:
      iteration = iteration + 1
      securityBreak = securityBreak + 1

      follower = followers[iteration]
    
      if self.check_user(follower) == True:
        follower['friendship_status']={}
        follower['profile_pic_url']=None
        follower['friendship_status']['following']=False
        follower['media'] = {}
        follower['media']['code'] = None
        follower['media']['image'] = None
        follower['media']['id'] = None
        filteredFollowers.append(follower)
      else:
        #delete the user from database
        self.logger.info('User is not valid, going to delete it from database')
        api_db.insert("delete from instagram_user_followers where id=%s",follower['id'])
        
      sleep_time = randint(1, 3)
      self.logger.info("Sleeping %s seconds" % sleep_time)
      time.sleep(sleep_time)
      self.logger.info("Current followers %s, iteration %s" % ( len(filteredFollowers), securityBreak))

    self.logger.info("Total received %s FILTERED followers" % len(filteredFollowers))
    filteredFollowers = filteredFollowers[:amount]
    
  
    bot_operation = 'follow_other_users_followers'
    return self.follow_users(filteredFollowers[:amount], bot_operation, userObject['username'])
    
    
def follow_users(self, users, bot_operation, bot_operation_value):
    broken_items = []

    # get followings list
    # result = api_db.select("select following_id from followings where id_user=%s",self.id_user)
    # followed_list = []
    # for i in result:
    #    followed_list.append(i['following_id'])

    # skipped_list = self.read_list_from_file(
    #    "skipped.txt")  # Read skipped.txt file
    self.logger.info("Going to follow %s users" % len(users))
    # remove skipped and already followed users  from user_ids
    # user_ids = list((set(user_ids) - set(followed_list)) - set(skipped_list))

    users = removeAlreadyFollowedUsers(users)

    self.logger.info("After removing already followed users, %s users left to follow." % len(users))

    totalFollowed = 0
    for user in tqdm(users):

        if not limits.check_if_bot_can_follow(self):
            self.logger.info("Out of follows for today.")
            break

        if self.follow(user):

            api_db.insertBotAction(self.id_campaign, self.web_application_id_user, user['instagram_id_user'], user['full_name'],
                                   user['username'],
                                   user['profile_pic_url'], user['media']['id'], user['media']['image'],
                                   user['media']['code'], bot_operation, bot_operation_value, self.id_log)
            totalFollowed = totalFollowed + 1
        else:
            broken_items.append(user)

    self.logger.info("DONE: Total followed %d users." % totalFollowed)
    self.logger.warning("Could not follow %d users." % len(broken_items))

    return totalFollowed


def removeAlreadyFollowedUsers(users):
    filteredList = []
    for u in users:
        if not u['friendship_status']['following']:
            filteredList.append(u)
    return filteredList


def follow_followers(self, user_id, nfollows=None):
    self.logger.info("Follow followers of: %s" % user_id)
    if not limits.check_if_bot_can_follow(self):
        self.logger.info("Out of follows for today.")
        return
    if not user_id:
        self.logger.info("User not found.")
        return
    follower_ids = self.get_user_followers(user_id, nfollows)
    if not follower_ids:
        self.logger.info("%s not found / closed / has no followers." % user_id)
    else:
        self.follow_users(follower_ids[:nfollows])


def follow_following(self, user_id, nfollows=None):
    self.logger.info("Follow following of: %s" % user_id)
    if not limits.check_if_bot_can_follow(self):
        self.logger.info("Out of follows for today.")
        return
    if not user_id:
        self.logger.info("User not found.")
        return
    following_ids = self.get_user_following(user_id)
    if not following_ids:
        self.logger.info("%s not found / closed / has no following." % user_id)
    else:
        self.follow_users(following_ids[:nfollows])


def getCurrentUserFollowing(self):
    result = api_db.select("select d.*  "
                           "from default_followings d "
                           "where d.id_user=%s", self.web_application_id_user)

    if len(result) < 1:
        self.logger.info("Getting current user following from database: empty set")
        return []
    else:
        resultArray = []
        self.logger.info("Getting current user following from database. Found %s records" % len(result))
        for item in result:
            resultArray.append(item['following_id'])
        return resultArray
