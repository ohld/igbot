from instaprole.instabot import API
from instaprole.bot_scheduler import BotScheduler
from instaprole.utils.generic_utils.singleton import Singleton


class BotSchedulerManager(metaclass=Singleton):

    def __init__(self):
        self.bot_schedulers = dict()  # One BotSchedule per user

    def create_scheduler(self, username, password):
        user_id = API().get_user_id_from_username(username)
        self.bot_schedulers[user_id] = BotScheduler(username, password)

    def get_scheduler(self, user_id):
        return self.bot_schedulers[user_id]

