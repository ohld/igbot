"""
    Like-and-follow-users methods
"""

import time
import random
from tqdm import tqdm

def like_and_follow(bot, user_id, nlikes=3):
    """
        Likes and follows <user_id>. Puts <nlikes> in his media.
    """
    bot.like_user_id(user_id, amount=nlikes)
    bot.follow(user_id)
    return True

def like_and_follow_media_likers(bot, media, nlikes=3):
    """
        Takes input media. Takes the list of the likers.
        Follows liker and like <nlikes> of his last posted medias.

        args:
            bot - instance of instabot.Bot() class
            nlikes - number of likes to put on each user's media
    """
    print ("Going to like & follow users who liked %s media" % media)
    bot.getMediaLikers(media)
    media_likers = [item['pk'] for item in bot.LastJson["users"]]
    print ("  I have %d likers of media." % len(media_likers))
    for user in tqdm(media_likers, desc="Media likers"):
        bot.like_and_follow(user)
        time.sleep(10 + 20 * random.random())
    return True

def like_and_follow_your_feed_likers(bot, nlikes=3):
    """
        Takes your last media. Takes the list of the likers.
        Follows liker and like <nlikes> of his last posted medias.

        args:
            bot - instance of instabot.Bot() class
            nlikes - number of likes to put on each user's media
    """
    print ("Going to like & follow users who like your last media")
    bot.getSelfUserFeed()
    last_media = bot.LastJson["items"][0]["pk"]
    return like_and_follow_media_likers(bot, last_media, nlikes=3)
