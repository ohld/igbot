"""
    instabot example

    Workflow:
        Like user's, follower's media by user_id.
"""

import sys
import os
import time
import random
from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

if len(sys.argv) < 2:
    print ("USAGE: Pass username(s).")
    print ("Example: python %s account1 account2" % sys.argv[0])
    exit()

bot = Bot()
bot.login()
for username in sys.argv[1:]:
    bot.like_followers(username, nlikes=3)
