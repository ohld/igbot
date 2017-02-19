"""
    instabot example

    Save checkpoint of your account - list of followers / followings.
"""

import sys
import os

sys.path.append(os.path.join(sys.path[0],'../../'))
from instabot import Bot

if len(sys.argv) != 2:
    print ("USAGE: Pass a path to the file where to save the checkpoint.")
    print ("Example: %s my_checkpoint" % sys.argv[0])
    exit()

bot = Bot()
bot.login()
bot.save_checkpoint(sys.argv[1])
