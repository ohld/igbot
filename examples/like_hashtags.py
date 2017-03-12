"""
    instabot example

    Workflow:
        Like last images with hashtag.
"""

import sys
import os
import time
import random
from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

if len(sys.argv) < 2:
    print ("USAGE: Pass hashtag(s) to like")
    print ("Example: python %s hashtag1 hashtag2" % sys.argv[0])
    exit()

bot = Bot()
bot.login()
for hashtag in sys.argv[1:]:
    bot.like_hashtag(hashtag)
