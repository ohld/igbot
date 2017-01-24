import time
import random

def like_timeline(bot, amount=None):
    """ Likes last 8 medias from timeline feed """
    print ("Liking timeline feed:")
    if amount is not None and amount > 8:
        amount = 8
        print ("  Can't request more than 8 medias from timeline... yet")
    if not bot.getTimelineFeed():
        print ("  Error while getting timeline feed")
        return False
    not_liked_feed = filter_not_liked(bot.LastJson["items"][:amount])
    return bot.like_medias(not_liked_feed)

def like_user_id(bot, user_id, amount=None):
    """ Likes last user_id's medias """
    print ("Liking user_%s's feed:" % user_id)
    if isinstance(user_id, int):
        user_id = str(user_id)
    if not user_id.isdigit():
        print ("You should pass user_id, not user's login.")
    if amount is not None and amount > 16:
        amount = 16
        print ("  Can't request more that 16 medias from user's feed... yet")
    bot.getUserFeed(user_id)
    if bot.LastJson["status"] == 'fail':
        print ("  This is a closed account")
        return False
    not_liked_feed = filter_not_liked(bot.LastJson["items"][:amount])
    return bot.like_medias(not_liked_feed)

def filter_not_liked(media_items):
    not_liked_medias = [item["pk"] for item in media_items if not item["has_liked"]]
    print ("  Recieved: %d. Already liked: %d." % (
                        len(media_items),
                        len(media_items) - len(not_liked_medias)
                        )
    )
    return not_liked_medias
