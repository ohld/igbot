"""
    instabot example

    Workflow:
        Like and follow likers of last medias from your timeline feed.
"""

import sys
import os
import time
import random
from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0],'../'))
from instabot import Bot

def like_and_follow(bot, user_id, nlikes=3):
    bot.like_user_id(user_id, amount=nlikes)
    bot.follow(user_id)
    return True

def like_and_follow_media_likers(bot, media, nlikes=3):
    for user in tqdm(bot.get_media_likers(media), desc="Media likers"):
        like_and_follow(bot, user)
        time.sleep(10 + 20 * random.random())
    return True

def like_and_follow_your_feed_likers(bot, nlikes=3):
    last_media = bot.get_your_medias()[0]
    return like_and_follow_media_likers(bot, last_media, nlikes=3)


bot = Bot()
bot.login()
like_and_follow_your_feed_likers(bot)
