from instabot.automation.tasks.follow_users_related_to_me import FollowUserRelatedToMe
from instabot.utils.generic_utils.random_utils import choose_random


class FollowFromFollowersOfMyFollowingAndPutLikes(FollowUserRelatedToMe):
    task_id = "follow_from_followers_of_my_following_and_put_likes"
    task_name = "Follow from followers of my following and put likes"

    def __init__(self, bot, config):
        super().__init__(bot, config)
        self.__relation_func__ = self.bot.get_user_followers

    def __compute_user_id__(self):
        return choose_random(self.bot.following)
