import time
import random
import json

def unfollow(self, user_id):
    if not self.check_user(user_id):
        return False
    if super(self.__class__, self).unfollow(user_id):
        self.total_unfollowed += 1
        return True
    return False

def unfollow_users(self, user_ids):
    """ user_ids - list of user_id to unfollow """
    logging.info("    Going to unfollow %d users." % len(user_ids))
    total_unfollowed = 0
    for user_id in tqdm(user_ids):
        if self.unfollow(user_id):
            total_unfollowed += 1
        else:
            pass
        time.sleep(15 + 30 * random.random())
    self.logger.info("    DONE: Total unfollowed %d users. " % total_unfollowed)
    return True

def unfollow_non_followers(bot):
  followings = set([item["pk"] for item in bot.getTotalSelfFollowings()])
  bot.logger.info("Unfollowing non-followers")
  bot.logger.info("  You follow %d users." % len(followings))
  followers = set([item["pk"] for item in bot.getTotalSelfFollowers()])
  bot.logger.info("  You are followed by %d users." % len(followers))
  diff = followings - followers
  bot.logger.info("  %d users don't follow you back." % len(diff))
  bot.unfollow_users(list(diff))
