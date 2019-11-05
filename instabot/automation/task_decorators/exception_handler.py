from instabot.automation.exceptions.task_exceptions import ActionBlockedException
from instabot.utils.generic_utils.abstract_decorator import AbstractDecorator


class ExceptionHandler(AbstractDecorator):

    def __do__(self, *args, **kwargs):
        print("ExceptionHandler - during wrapper")
        task = args[0]
        task_name = task.task_name
        bot = task.bot
        config = task.config
        try:
            self.function(task)
        except ActionBlockedException as e:
            bot.logger.info("TASK [STOPPED] -> `{}` has stopped because of {}".format(task_name, e.__cause__))

