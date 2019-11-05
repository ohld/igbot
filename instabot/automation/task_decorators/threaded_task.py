import threading

from instabot.utils.generic_utils.abstract_decorator import AbstractDecorator


class ThreadedTask(AbstractDecorator):

    def __do__(self, *args, **kwargs):
        print("ThreadedTask - during wrapper")
        task = args[0]
        task_name = task.task_name
        bot = task.bot
        config = task.config
        bot.logger.info("TASK [STARTING] -> `{}` will be run threaded...".format(task_name))
        job_thread = threading.Thread(target=self.function, args=(task,))
        job_thread.start()

