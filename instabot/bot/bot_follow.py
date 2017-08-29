from tqdm import tqdm

from . import limits
from . import delay
from ..api import api_db

def follow(self, user_id):
    user_id = self.convert_to_user_id(user_id)
    self.logger.info('Going to Follow user_id: %s ' % (user_id))
    if not self.check_user(user_id):
        return True
    if limits.check_if_bot_can_follow(self):
        delay.follow_delay(self)
        if super(self.__class__, self).follow(user_id):
            self.logger.info("Followed user with id: %s" % user_id)
            self.total_followed += 1
            api_db.insert("insert into followings (id_campaign,id_user,following_id) values (%s,%s,%s)", self.id_campaign,self.id_user,user_id)
            return True
    else:
        self.logger.info("Out of follows for today.")
    return False


def follow_users(self, user_ids):
    broken_items = []
    if not limits.check_if_bot_can_follow(self):
        self.logger.info("Out of follows for today.")
        return

    #get followings list
    result = api_db.select("select following_id from followings where id_user=%s",self.id_user)
    followed_list = []
    for i in result:
        followed_list.append(i['following_id'])

    skipped_list = self.read_list_from_file(
        "skipped.txt")  # Read skipped.txt file
    self.logger.info("Going to follow %s users" % len(user_ids))
    # remove skipped and already followed users  from user_ids
    user_ids = list((set(user_ids) - set(followed_list)) - set(skipped_list))
    self.logger.info("After filtering followedlist and skippedlist.txt,  %s  users left to follow." % len(
        user_ids))

    for user_id in tqdm(user_ids):
        if not self.follow(user_id):
            self.logger.info("This id %s is a broken item" % user_id)
            delay.error_delay(self)
            broken_items = user_ids[user_ids.index(user_id):]
            break

    self.logger.info("DONE: Total followed %d users." % self.total_followed)
    return broken_items


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
                             "where d.id_user=%s",self.id_user)

    if len(result)<1:
        self.logger.info("Getting current user following from database: empty set")
        return []
    else:
        resultArray = []
        self.logger.info("Getting current user following from database. Found %s records" % len(result))
        for item in result:
            resultArray.append(item['following_id'])
        return resultArray