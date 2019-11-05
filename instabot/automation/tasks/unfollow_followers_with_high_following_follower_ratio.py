from instabot.automation.task import Task
from instabot.utils.generic_utils.random_utils import choose_random
from instabot.utils.list_utils.list_utils import ListUtils


class UnfollowFollowersWithHighFollowingFollowerRatio(Task):
    task_id = "unfollow_followers_with_high_following_follower_ratio"
    task_name = "Unfollow followers with high following / follower Ratio"

    def do(self):
        user_to_unfollow = self.config["number_of_users_to_unfollow"]
        # We take only people that follow us and followed by us
        followers_following = ListUtils.commons(self.bot.followers, self.bot.following)
        if len(followers_following) < self.config["number_of_users_to_unfollow"]:
            user_to_unfollow = len(followers_following)
        followers_to_unfollow = choose_random(followers_following, k=user_to_unfollow)
        for user_id in followers_to_unfollow:
            user_info = self.bot.get_user_info(user_id)
            follower_count = user_info["follower_count"]
            following_count = user_info["following_count"]
            if follower_count != 0:
                ratio = float(following_count / follower_count)
                if ratio > self.config["ratio"]:
                    self.bot.unfollow(user_id)


