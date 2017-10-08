from tqdm import tqdm

from . import limits
from . import delay
from ..api import api_db


def follow(self, user):
    self.logger.info('Going to Follow user: %s ' % user['username'])

    #this returns 404 , why ?
    #if not self.check_user(user):
    #    return False

    delay.follow_delay(self)
    if super(self.__class__, self).follow(user['pk']):
        self.logger.info("Successfully followed user %s " % user['username'])
        self.total_followed += 1
        return True

    return False


def follow_users_by_location(self, locationObject, amount):
    self.logger.info("Going to follow %s users from location %s." % (amount, locationObject['name']))

    medias = self.getLocationFeed(locationObject['id'],amount)

    users = []

    for media in medias:
        user = media['user']
        user['media'] = {}
        user['instagram_user_id']=media['pk']
        user['media']['code'] = media['code']
        user['media']['image'] = media['image_versions2']['candidates'][0]['url']
        user['media']['id'] = media['pk']
        users.append(user)

    bot_operation = 'follow_users_by_location'
    return self.follow_users(users[:amount], bot_operation, locationObject['name'])

def follow_users_by_hashtag(self,hashtag,amount):
    feed = self.getHashtagFeed(hashtag, amount)
    users = []

    for media in feed:
        user = media['user']
        user['media'] = {}
        user['instagram_user_id'] = media['pk']
        user['media']['code'] = media['code']
        user['media']['image'] = media['image_versions2']['candidates'][0]['url']
        user['media']['id'] = media['pk']
        users.append(user)
    bot_operation = 'follow_users_by_hashtag'

    return self.follow_users(users[:amount], bot_operation, hashtag)

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

            api_db.insertBotAction(self.id_campaign, self.web_application_id_user, user['pk'], user['full_name'],
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
