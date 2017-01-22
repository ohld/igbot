import time
import random

def like_timeline(bot):
    """ Likes last 8 medias from timeline feed """
    print ("Liking timeline feed:")
    if not bot.getTimelineFeed():
        print ("  Error while getting timeline feed")
        return False
    not_liked_feed = [item["pk"] for item in bot.LastJson["items"] if not item["has_liked"]]
    print ("  Recieved: %d. Already liked: %d." % (
                        len(bot.LastJson["items"]),
                        len(bot.LastJson["items"]) - len(not_liked_feed)
                        )
    )
    return bot.like_medias(not_liked_feed)

def like_user_id(bot, user_id):
    """ Likes last username's medias """
    print ("Liking user_%s's feed:" % user_id)
    if not user_id.isdigit():
        print ("You should pass user_id, not user's login.")
    bot.getUserFeed(user_id)
    not_liked_feed = [item["pk"] for item in bot.LastJson["items"] if not item["has_liked"]]
    print ("  Recieved: %d. Already liked: %d." % (
                        len(bot.LastJson["items"]),
                        len(bot.LastJson["items"]) - len(not_liked_feed)
                        )
    )
    return bot.like_medias(not_liked_feed)
