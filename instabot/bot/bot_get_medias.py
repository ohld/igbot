"""
    All methods must return media_ids that can be
    passed into e.g. like() or comment() functions.
"""

from . import limits

def filter_not_liked(media_items, log=False):

    not_liked_medias = []

    for m in media_items:
        if 'pk' in m.keys():
            if 'has_liked' in m.keys():
                if not m['has_liked']:
                    if m['like_count'] <= limits.MAX_LIKES_TO_LIKE:
                        not_liked_medias.append(m['pk'])
        else:
            # this has no pk and is a list of suggestions
            if m['type'] == 3:
                print("Skipping suggestions.")
            else:
                # depending on type, we may get other types of objects here
                print("Unknown object detected.")
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

def get_hashtag_medias(bot, hashtag, amount):

    if not bot.getHashtagFeed(hashtag):
         print ("Error while getting hashtag feed")
         return False
    return filter_not_liked(bot.LastJson["items"])
    
