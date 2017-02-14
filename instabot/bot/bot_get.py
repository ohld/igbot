"""
    All methods must return media_ids that can be
    passed into e.g. like() or comment() functions.
"""

from . import limits

# filters

def filter_not_liked(media_items, log=False):
    # TODO: convert these print function to logging

    not_liked_medias = []
    for m in media_items:
        if 'pk' in m.keys():
            if 'has_liked' in m.keys():
                if not m['has_liked']:
                    if m['like_count'] <= limits.MAX_LIKES_TO_LIKE:
                        not_liked_medias.append(m['pk'])
    if log:
        print ("  Recieved: %d. Already liked: %d." % (
                            len(media_items),
                            len(media_items) - len(not_liked_medias)
                            )
        )
    return not_liked_medias

def filter_media(media_items, log=False):
    # TODO: should return not liked and not commented medias
    # remove filter_not_liked when implemented
    return filter_not_liked(media_items, log=False)

def filter_users(user_items, log=False):
    # TODO: filter users from blacklist and already subscribed
    pass

# getters

def get_timeline_medias(bot):
    if not bot.getTimelineFeed():
        bot.logger.info("  Error while getting timeline feed")
        return False
    return filter_media(bot.LastJson["items"])

def get_user_medias(bot, user_id):
    bot.getUserFeed(user_id)
    if bot.LastJson["status"] == 'fail':
        bot.logger.info("  This is a closed account")
        return False
    return filter_media(bot.LastJson["items"])

def get_hashtag_medias(bot, hashtag):
    if not bot.getHashtagFeed(hashtag):
         bot.logger.info("Error while getting hashtag feed")
         return False
    return filter_media(bot.LastJson["items"])

def get_geotag_medias(bot, geotag):
    # TODO: returns list of medias from geotag
    pass

def get_timeline_users(bot):
    # TODO: returns list userids who just posted on your timeline feed
    pass

def get_hashtag_users(bot, hashtag):
    # TODO: returns list userids who just posted on this hashtag
    pass

def get_geotag_users(bot, geotag):
    # TODO: returns list userids who just posted on this geotag
    pass

def get_user_followers(bot, user_id):
    # TODO: return a list of user's followers
    pass

def get_user_following(bot, user_id):
    # TODO: return a list of user's following
    pass
