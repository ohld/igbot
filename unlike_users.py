"""
    instabot example

    Workflow:
        Unlike last media's of users.
"""

import sys
import os
import time
import random
from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

if len(sys.argv) < 2:
    print ("USAGE: Pass username(s) to unlike.")
    print ("Example: python %s account1 account2" % sys.argv[0])
    exit()

bot = Bot()
bot.login()
for username in sys.argv[1:]:
    bot.unlike_user(username)
