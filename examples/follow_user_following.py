"""
    instabot example

    Workflow:
        Follow user's following by username.
"""

import sys
import os
import time
import random
from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

if len(sys.argv) < 2:
    print ("USAGE: username of account to follow the followings of / username of (your) specific account.")
    print ("Example: python %s competitor youraccount" % sys.argv[0])
    exit()

bot = Bot()
bot.login()
for username in sys.argv[1:]:
    bot.follow_following(username)
