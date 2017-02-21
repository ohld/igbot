from tqdm import tqdm

from . import limits
from . import delay

def unfollow(self, user_id):
    user_id = self.convert_to_user_id(user_id)
    if not self.check_user(user_id):
        return True
    if limits.check_if_bot_can_unfollow(self):
        delay.unfollow_delay(self)
        if super(self.__class__, self).unfollow(user_id):
            self.total_unfollowed += 1
            return True
    else:
        self.logger.info("Out of unfollows for today.")
    return False

def unfollow_users(self, user_ids):
    self.logger.info("Going to unfollow %d users." % len(user_ids))
    total_unfollowed = 0
    for user_id in tqdm(user_ids):
        if not self.unfollow(user_id):
            delay.error_delay(self)
            while not self.unfollow(user_id):
                delay.error_delay(self)
    self.logger.info("DONE: Total unfollowed %d users. " % total_unfollowed)
    return True

def unfollow_non_followers(self):
    bot.logger.info("Unfollowing non-followers")
    followings = set([item["pk"] for item in bot.getTotalSelfFollowings()])
    bot.logger.info("You follow %d users." % len(followings))
    followers = set([item["pk"] for item in bot.getTotalSelfFollowers()])
    bot.logger.info("You are followed by %d users." % len(followers))
    diff = followings - followers
    bot.logger.info("%d users don't follow you back." % len(diff))
    bot.unfollow_users(list(diff))

def unfollow_everyone(self):
    your_following = bot.get_user_following(bot.user_id)
    bot.unfollow_users(your_following)
