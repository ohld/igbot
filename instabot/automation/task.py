from abc import ABC, abstractmethod

from instabot.automation.task_decorators.bot_task import BotTask
from instabot.automation.task_decorators.exception_handler import ExceptionHandler
from instabot.automation.task_decorators.threaded_task import ThreadedTask


class Task(ABC):
    task_id = "task_id"
    task_name = "task_name"

    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

    @BotTask
    @ThreadedTask
    @ExceptionHandler
    def execute(self):
        self.do()

    @abstractmethod
    def do(self):
        pass

    def __repr__(self):
        return "task_name: " + self.task_name
