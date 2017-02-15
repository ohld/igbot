import time
import random
import json
from tqdm import tqdm

def follow(self, user_id):
    if not self.check_user(user_id):
        return False
    if super(self.__class__, self).follow(user_id):
        self.total_followed += 1
        return True
    return False

def follow_users(self, user_ids):
    """ user_ids - list of user_id to follow """
    self.logger.info("    Going to follow %d users." % len(user_ids))
    total_followed = 0
    for user_id in tqdm(user_ids):
        if self.follow(user_id):
            total_followed += 1
        else:
            pass
        time.sleep(15 + 30 * random.random())
    self.logger.info("    DONE: Total followed %d users. " % total_followed)
    return True

def follow_followers(self, user_id, nfollows=40):
    if not user_id:
        return False

    self.logger.info("Follow followers of: %i" % user_id)

    followers = self.getTotalFollowers(user_id)
    follower_ids = []

    for f in followers:
    	follower_ids.append(f['pk'])

    # slice up followers
    follower_ids = follower_ids[0:nfollows]

    for i in tqdm(follower_ids, desc="Following followers"):
    	self.logger.info("Following %i's feed:" % i)
    	self.follow(i)
    	time.sleep(10 + 20 * random.random())
