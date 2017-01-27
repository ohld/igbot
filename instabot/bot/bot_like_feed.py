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
    if amount is not None and amount > 8:
        amount = 8
        print ("  Can't request more than 8 medias from timeline... yet")
    medias = bot.get_timeline_medias()[:amount]
    return bot.like_medias(medias)

def like_user_id(bot, user_id, amount=None):
    """ Likes last user_id's medias """
    user_id = check_user_id(user_id)
    if not user_id:
        return False
    print ("Liking user_%s's feed:" % user_id)
    if amount is not None and amount > 16:
        amount = 16
        print ("  Can't request more that 16 medias from user's feed... yet")
    medias = bot.get_user_medias(user_id)[:amount]
    return bot.like_medias(medias)
