"""
    instabot example

    Workflow:
        Like last medias by user.
"""

import sys
import os
import time
import random
from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0],'../'))
from instabot import Bot

if len(sys.argv) != 2:
    print ("USAGE: Pass user to like")
    print ("Example: python %s ohld" % sys.argv[0])
    exit()

bot = Bot()
bot.login()
bot.like_user_id(sys.argv[1])
