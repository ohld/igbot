"""
    instabot example

    Workflow:
        Like and follow you last media likers.
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

if len(sys.argv) != 2:
    print ("USAGE: Pass media_id")
    print ("Example: %s 123123123123" % sys.argv[0])
    exit()

bot = Bot()
bot.login()
like_and_follow_media_likers(bot, sys.argv[1])
