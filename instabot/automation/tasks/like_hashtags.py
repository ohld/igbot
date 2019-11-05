from instabot.automation.exceptions.task_exceptions import NoResultFoundException
from instabot.automation.task import Task
from instabot.data.models.elements.hashtag import Hashtag
from instabot.data.mongo.mongo_serializer import convert
from instabot.data.mongo.operations.mongooperations import MongoFind
from instabot.utils.generic_utils.random_utils import choose_random


class LikeHashtags(Task):
    task_id = "like_hashtags"
    task_name = "Put like to a random chosen hashtag"

    def do(self):
        """ Randomly choose an hashtag from the list and put likes to the first <amount> posts, if they match the
        instabot conditions """
        amount = self.config["like_amount"]
        hashtags = convert(Hashtag, MongoFind(database_name=self.bot.user_id, collection_name=self.bot.HASHTAGS).do(
            query={"blacklist": False}))
        hashtag = choose_random(hashtags)
        hashtag_name = hashtag.id
        self.bot.logger.info("BOT-SCHEDULE - Liking {} posts for hashtag {}".format(amount, hashtag_name))

        medias = self.bot.get_total_hashtag_medias(hashtag_name)
        if self.bot.api.search_tags(hashtag_name):
            for tag in self.bot.api.last_json["results"]:
                if tag["name"] == hashtag_name:
                    hashtag_id = tag["id"]
                    break
            counter = 0
            if len(medias) < amount:
                amount = len(medias)
            while counter != amount:
                media = medias[counter]
                result = self.bot.like(media, check_media=False, hashtag_id=hashtag_id,
                                  hashtag_name=hashtag_name, container_module="feed_contextual_hashtag")
                if result is True:
                    counter = counter + 1
        else:
            self.bot.logger.error("BOT-SCHEDULE - No info for hashtag: {}".format(hashtag_name))
            raise NoResultFoundException
