from instabot.automation.task import Task


class LikeTimeline(Task):
    task_id = "like_timeline"
    task_name = "Put like to your timeline"

    def do(self):
        """ Put likes to the first <amount> posts in the feed, if they match the instabot conditions """
        amount = self.config["like_amount"]
        self.bot.logger.info("BOT-SCHEDULE - Liking timeline feed for {} posts".format(amount))
        medias = self.bot.get_timeline_medias()
        counter = 0
        if len(medias) < amount:
            amount = len(medias)
        while counter != amount:
            media = medias[counter]
            result = self.bot.like(media, check_media=False)
            if result is True:
                counter = counter + 1
