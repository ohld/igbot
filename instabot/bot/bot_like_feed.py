import time
import random

def like_timeline(bot, amount=None):
    """ Likes last 8 medias from timeline feed """
    bot.logger.info("Liking timeline feed:")
    medias = bot.get_timeline_medias()[:amount]
    return bot.like_medias(medias)

def like_user_id(bot, user_id, amount=None):
    """ Likes last user_id's medias """
    if not user_id:
        return False
    bot.logger.info("Liking user_%s's feed:" % user_id)
    medias = bot.get_user_medias(user_id)
    if not medias:
        bot.logger.info("  Can't like user: account is closed!")
        return False
    return bot.like_medias(medias[:amount])

def like_hashtag(bot, hashtag, amount=None):
    bot.logger.info("Going to like media with hashtag #%s" % hashtag)
    medias = bot.get_hashtag_medias(hashtag)
    return bot.like_medias(medias[:amount])

def comment_hashtag(bot, hashtag, amount=None):
    bot.logger.info("Going to comment medias by %s hashtag" % hashtag)
    medias = bot.get_hashtag_medias(hashtag)
    return bot.comment_medias(medias[:amount])
