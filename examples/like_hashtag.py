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

sys.path.append(os.path.join(sys.path[0],'../'))
from instabot import Bot

if len(sys.argv) != 2:
    print ("USAGE: Pass hashtag to like")
    print ("Example: %s dog" % sys.argv[0])
    exit()

bot = Bot()
bot.login()
bot.like_hashtag(sys.argv[1])
