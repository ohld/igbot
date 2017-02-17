"""
    instabot example

    Workflow:
        Follow user's followers by user_id.
"""

import sys
import os
import time
import random
from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0],'../'))
from instabot import Bot

if len(sys.argv) != 2:
    print ("USAGE: Pass user_id")
    print ("Example: %s 352300017" % sys.argv[0])
    exit()

bot = Bot()
bot.login()
bot.follow_followers(sys.argv[1])
