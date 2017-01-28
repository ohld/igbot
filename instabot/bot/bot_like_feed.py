import time
import random

def check_user_id(user_id):
    if isinstance(user_id, int):
        user_id = str(user_id)
    if not user_id.isdigit():
        print ("You should pass user_id, not user's login.")
        return False
    return user_id

def like_timeline(bot, amount=None):
    """ Likes last 8 medias from timeline feed """
    print ("Liking timeline feed:")
    medias = bot.get_timeline_medias()[:amount]
    return bot.like_medias(medias)

def like_user_id(bot, user_id, amount=None):
    """ Likes last user_id's medias """
    user_id = check_user_id(user_id)
    if not user_id:
        return False
    print ("Liking user_%s's feed:" % user_id)
    medias = bot.get_user_medias(user_id)
    if not medias:
        print ("  Can't like user: account is closed!")
        return False
    return bot.like_medias(medias[:amount])

def like_hashtag(bot, hashtag, amount=None):
    print ("Going to like medias by %s hashtag" % hashtag)
    medias = bot.get_hashtag_medias(bot, hashtag)
    return bot.like_medias(medias[:amount])
