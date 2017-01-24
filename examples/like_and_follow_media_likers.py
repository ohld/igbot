"""
    instabot example

    Workflow:
        1) creates checkpoint: saves your current followings
        2) like and follow you last media likers
        3) reverts to checkpoint: unfollow new followings.
"""

import sys
import os
import time
import random
from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0],'../'))
from instabot import Bot

bot = Bot()
bot.login()
bot.save_checkpoint()
bot.like_and_follow_your_feed_likers()
cp = bot.load_last_checkpoint()
bot.revert_to_checkpoint(cp)
bot.logout()
