from abc import abstractmethod

from instabot.automation.task import Task
from instabot.utils.generic_utils.random_utils import choose_random
from instabot.utils.list_utils.list_utils import ListUtils


class FollowUserRelatedToMe(Task):
    task_id = "follow_users_related_to_me"
    task_name = "Follow users related to me"

    def __init__(self, bot, config):
        super().__init__(bot, config)
        self.__relation_func__ = None

    @abstractmethod
    def __compute_user_id__(self):
        pass

    def do(self):
        """" Follow <n> of a user's related guys and put likes to their photos. relation_func is supposed to receive as\
         first argument the user_id and as last arguments the arguments relation_func_extra_args """
        user_id = self.__compute_user_id__()
        nfollows = self.config["number_of_users_to_follow"]
        self.bot.logger.info("TASK -> {}. Follow guys related to: {}".format(self.task_name, user_id))
        if self.bot.reached_limit("follows"):
            self.bot.logger.info("TASK -> {}. Out of follows for today.".format(self.task_name))
            return
        if not user_id:
            self.bot.logger.wanr("TASK -> {}. User not found.".format(self.task_name))
            return
        related_guys = self.__relation_func__(user_id, nfollows)
        related_guys = ListUtils.diff(related_guys - self.bot.blacklist)
        if not related_guys:
            self.bot.logger.info(
                "TASK -> {}. {} not found / closed / has no related guys.".format(self.task_name, user_id))
        else:
            users_to_follow = related_guys[:nfollows]
            for user_to_follow in users_to_follow:
                user_medias = self.bot.get_user_medias(user_to_follow)
                if user_medias:
                    if self.config["put_likes_to_recent_posts"] > 0:
                        user_medias_recents = user_medias[:self.config["window_likes_size"]]
                        user_medias_to_like = choose_random(user_medias_recents,
                                                            k=self.config["put_likes_to_recent_posts"])
                        self.bot.like_medias(user_medias_to_like)
                    if self.config["put_likes_to_remote_posts"] > 0:
                        user_medias_remotes = user_medias[-self.config["window_likes_size"]:]
                        user_medias_to_like = choose_random(user_medias_remotes,
                                                            k=self.config["put_likes_to_remote_posts"])
                        self.bot.like_medias(user_medias_to_like)
                    self.bot.follow(user_to_follow)
