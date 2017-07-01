from tqdm import tqdm

from . import limits
from . import delay


def unfollow(self, user_id):
    user_id = self.convert_to_user_id(user_id)
    if self.check_user(user_id):
        return True  # whitelisted user
    if limits.check_if_bot_can_unfollow(self):
        delay.unfollow_delay(self)
        if super(self.__class__, self).unfollow(user_id):
            self.total_unfollowed += 1
            return True
    else:
        self.logger.info("Out of unfollows for today.")
    return False


def unfollow_users(self, user_ids):
    broken_items = []
    self.logger.info("Going to unfollow %d users." % len(user_ids))
    user_ids = set(map(str, user_ids))
    filtered_user_ids = list(set(user_ids) - set(self.whitelist))
    if len(filtered_user_ids) != len(user_ids):
        self.logger.info("After filtration by whitelist %d users left." % len(filtered_user_ids))
    for user_id in tqdm(filtered_user_ids):
        if not self.unfollow(user_id):
            delay.error_delay(self)
            broken_items = filtered_user_ids[filtered_user_ids.index(user_id):]
            break
    self.logger.info("DONE: Total unfollowed %d users. " %
                     self.total_unfollowed)
    return broken_items


def unfollow_non_followers(self):
    self.logger.info("Unfollowing non-followers")
    followings = set([item["pk"] for item in self.getTotalSelfFollowings()])
    self.logger.info("You follow %d users." % len(followings))
    followers = set([item["pk"] for item in self.getTotalSelfFollowers()])
    self.logger.info("You are followed by %d users." % len(followers))
    diff = followings - followers
    self.logger.info("%d users don't follow you back." % len(diff))
    self.unfollow_users(list(diff))


def unfollow_everyone(self):
    self.following = self.get_user_following(self.user_id)
    self.unfollow_users(self.following)
