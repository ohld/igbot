"""
    instabot example

    Workflow:
        Follow users who post medias with hashtag.
"""

import sys
import os
import time
import random
from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

if len(sys.argv) < 2:
    print ("USAGE: Pass hashtag / hashtags.")
    print ("Example: python %s dog cat" % sys.argv[0])
    exit()

bot = Bot()
bot.login()
for hashtag in sys.argv[1:]:
    users = bot.get_hashtag_users(hashtag)
    bot.follow_users(users)
