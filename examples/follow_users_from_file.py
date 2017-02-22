"""
    instabot example

    Workflow:
        Take users from input file and follow them.
        The file should contain one username per line!
"""

import sys
import os

sys.path.append(os.path.join(sys.path[0],'../'))
from instabot import Bot

if len(sys.argv) != 2:
    print ("USAGE: Pass a path to the file with usernames")
    print ("Example: python %s users_to_follow.txt" % sys.argv[0])
    exit()

bot = Bot()
users_to_follow = bot.read_list_from_file(sys.argv[1])
if not users_to_follow:
    exit()
bot.login()
bot.follow_users(users_to_follow)
