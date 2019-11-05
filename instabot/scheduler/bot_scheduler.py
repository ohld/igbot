import copy

import schedule
import time

from instabot.automation.task_importer import TaskImporter
from instabot import Bot, API
#from instabot.data.models.config.configuration import Configuration
#from instabot.data.mongo.operations.mongooperations import MongoFind, MongoCreateIndex
#from instabot.data.mongo.mongo_serializer import convert

from instabot.utils.logger.logger import Logger
from instabot.utils.time_utils.datetime_utils import DatetimeUtils


class BotScheduler:

    TASKS_DIRECTORY = "instabot/automation/tasks"

    def __init__(self, username, password, configuration):
        self.user_id = API().get_user_id_from_username(username)
        self.configuration = configuration
        self.logger = Logger().get_logger(logger_id=self.__class__.__name__,
                                          log_path=self.configuration.bot_params["base_path"])
        self.bots = dict()
        self.bots["original"] = self.__create_bot__()
        self.__login__(username, password)

    def __create_bot__(self):
        bot = Bot(
            base_path=self.configuration.bot_params["base_path"],
            proxy=self.configuration.bot_params["proxy"],
            max_likes_per_day=self.configuration.bot_params["max_likes_per_day"],
            max_unlikes_per_day=self.configuration.bot_params["max_unlikes_per_day"],
            max_follows_per_day=self.configuration.bot_params["max_follows_per_day"],
            max_unfollows_per_day=self.configuration.bot_params["max_unfollows_per_day"],
            max_comments_per_day=self.configuration.bot_params["max_comments_per_day"],
            max_blocks_per_day=self.configuration.bot_params["max_blocks_per_day"],
            max_unblocks_per_day=self.configuration.bot_params["max_unblocks_per_day"],
            max_likes_to_like=self.configuration.bot_params["max_likes_to_like"],
            min_likes_to_like=self.configuration.bot_params["min_likes_to_like"],
            max_messages_per_day=self.configuration.bot_params["max_messages_per_day"],
            filter_users=self.configuration.bot_params["filter_users"],
            filter_private_users=self.configuration.bot_params["filter_private_users"],  # True if you want to skip
            filter_users_without_profile_photo=self.configuration.bot_params["filter_users_without_profile_photo"],
            # True if you want to skip
            filter_previously_followed=self.configuration.bot_params["filter_previously_followed"],
            # True if you want to skip
            filter_business_accounts=self.configuration.bot_params["filter_business_accounts"],
            # True if you want to skip
            filter_verified_accounts=self.configuration.bot_params["filter_verified_accounts"],
            # True if you want to skip
            max_followers_to_follow=self.configuration.bot_params["max_followers_to_follow"],
            min_followers_to_follow=self.configuration.bot_params["min_followers_to_follow"],
            max_following_to_follow=self.configuration.bot_params["max_following_to_follow"],
            min_following_to_follow=self.configuration.bot_params["min_following_to_follow"],
            max_followers_to_following_ratio=self.configuration.bot_params["max_followers_to_following_ratio"],
            max_following_to_followers_ratio=self.configuration.bot_params["max_following_to_followers_ratio"],
            min_media_count_to_follow=self.configuration.bot_params["min_media_count_to_follow"],
            max_following_to_block=self.configuration.bot_params["max_following_to_block"],
            like_delay=self.configuration.bot_params["like_delay"],
            unlike_delay=self.configuration.bot_params["unlike_delay"],
            follow_delay=self.configuration.bot_params["follow_delay"],
            unfollow_delay=self.configuration.bot_params["unfollow_delay"],
            comment_delay=self.configuration.bot_params["comment_delay"],
            block_delay=self.configuration.bot_params["block_delay"],
            unblock_delay=self.configuration.bot_params["unblock_delay"],
            message_delay=self.configuration.bot_params["message_delay"],
            blocked_actions_protection=self.configuration.bot_params["blocked_actions_protection"],
            # Block request if a block is detected
            verbosity=self.configuration.bot_params["verbosity"],  # en
            device=self.configuration.bot_params["device"],  # get default (one_plus_7)
            save_logfile=self.configuration.bot_params["save_logfile"]
        )
        return bot

    def __login__(self, username, password):
        self.bots["original"].login(username=username, password=password, force=False, use_cookie=True)

    def run(self, schedule_config):
        for task_name, task in self.configuration.task_params["schedule_config"].items():
            if task["active"]:
                self.bots[task_name] = copy.deepcopy(self.bots["original"])
                self.bots[task_name].task_name = task_name
                self.logger.info("BOT-SCHEDULER - Enabling schedule: <{}> every: {} {}"
                                 .format(task["function_name"], task["schedule"]["value"],
                                         task["schedule"]["time_unit"]))
                bot_function = getattr(bot_functions, task["function_name"])
                scheduler = schedule.every(task["schedule"]["value"])
                setattr(scheduler, "unit", task["schedule"]["time_unit"])
                # Schedule a task with the following inputs:
                #  - bot related to that task,
                #  - configuration related to that task (scope limiting)
                scheduler.do(bot_function, task_name, self.bots[task_name],
                             self.configuration.task_params["task_config"][task_name])

        while True:
            schedule.run_pending()
            time.sleep(1)

    def execute(self, task_id):
        self.bots[task_id] = copy.deepcopy(self.bots["original"])
        #job_fn(task_name, self.bots["single_execution"], self.configuration.task_params["task_config"][task_name])

        tasks = TaskImporter.import_tasks(self.TASKS_DIRECTORY)
        try:
            task = tasks[task_id]
            task(self.bots[task_id], self.configuration.task_params["task_config"][task_id]).execute()
        except KeyError:
            self.logger.error("BOT-SCHEDULER - No task with id {} found. Abort.".format(task_id))

    def execute_multiple(self, task_ids):
        for task_id in task_ids:
            self.execute(task_id)
