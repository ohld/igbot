"""
    instabot example

    Workflow:
        Take users from input file and follow them.
        The file should contain one user_id per line!
"""

import sys
import os
import io
import time
import random
from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0],'../'))
from instabot import Bot

if len(sys.argv) != 2:
    print ("USAGE: Pass a path to the file with user_ids")
    print ("Example: %s users_to_follow.txt" % sys.argv[0])
    exit()

users_file_name = sys.argv[1]
if not os.path.exists(users_file_name):
    print ("Can't find '%s' file." % users_file_name)
    exit()

if users_file_name:
    if os.path.exists(users_file_name):
        with io.open(users_file_name, "r", encoding="utf8") as f:
            users_to_follow = f.readlines()
    else:
        self.logger.info("Can't find file with user_ids!")
        exit()

bot = Bot()
bot.login()
bot.follow_users(users_to_follow)
