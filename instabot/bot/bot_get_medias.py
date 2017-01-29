"""
    All methods must return media_ids that can be
    passed into e.g. like() or comment() functions.
"""

def filter_not_liked(media_items, log=False):
    not_liked_medias = [item["pk"] for item in media_items if not item["has_liked"]]
    if log:
        print ("  Recieved: %d. Already liked: %d." % (
                            len(media_items),
                            len(media_items) - len(not_liked_medias)
                            )
        )
    return not_liked_medias

def get_timeline_medias(bot):
    if not bot.getTimelineFeed():
        print ("  Error while getting timeline feed")
        return False
    return filter_not_liked(bot.LastJson["items"])

def get_user_medias(bot, user_id):
    bot.getUserFeed(user_id)
    if bot.LastJson["status"] == 'fail':
        print ("  This is a closed account")
        return False
    return filter_not_liked(bot.LastJson["items"])

def get_hashtag_medias(bot, hashtag):
    if not bot.getHashtagFeed(hashtag):
        print ("Error while getting hashtag feed")
        return False
    return filter_not_liked(bot.LastJson["items"])
