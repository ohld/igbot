"""
    instabot example

    Reverts to checkpoint of your account - unfollows to old following
"""

import sys
import os

sys.path.append(os.path.join(sys.path[0],'../../'))
from instabot import Bot

if len(sys.argv) != 2:
    print ("USAGE: Pass a path to the checkpoint.")
    print ("Example: %s my_checkpoint" % sys.argv[0])
    exit()

bot = Bot()
if not bot.check_if_file_exists(sys.argv[1]):
    exit()
bot.login()
bot.revert_to_checkpoint(sys.argv[1])
