"""
    instabot example

    Workflow:
        1) Saves checkpoint
        2) follows some users
        3) loads checkpoint
        4) unfollows new users.
"""

import sys
import os

sys.path.append(os.path.join(sys.path[0],'../'))
from instabot import Bot

bot = Bot()
bot.login()
bot.save_checkpoint()
bot.follow_users(["2188662326", "6424540"])
cp = bot.load_last_checkpoint()
bot.revert_to_checkpoint(cp)
