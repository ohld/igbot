import time
import random

def like_hashtag(bot, hashtag):
    print ("Going to like medias by %s hashtag" % hashtag)
    if not bot.getHashtagFeed(hashtag):
        print ("Error while getting hashtag feed")
        return False
    not_liked_feed = [item["pk"] for item in bot.LastJson["items"] if not item["has_liked"]]
    print ("  Recieved: %d. Already liked: %d." % (
                        len(bot.LastJson["items"]),
                        len(bot.LastJson["items"]) - len(not_liked_feed)
                        )
    )
    return bot.like_medias(not_liked_feed)
