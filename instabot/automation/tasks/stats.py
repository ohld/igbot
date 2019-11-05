from instabot.automation.task import Task


class Stats(Task):
    task_id = "stats"
    task_name = "Compute statistics"

    def do(self):
        """ Compute stats and save it on MongoDB collection named "statistics" """
        self.bot.save_user_stats(self.bot.user_id)
