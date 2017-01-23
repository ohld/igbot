"""
    Example checkpoints usage:
    Saves checkpoint, follow some users, loads checkpoint, unfollows new users.
"""

import sys
import os

sys.path.append(os.path.join(sys.path[0],'../'))
from instabot import Bot

bot = Bot()
bot.login()
# saves checkpoint
bot.save_checkpoint()
# follow some users
bot.follow_users(["2188662326", "6424540"])
# load saved checkpoint
cp = bot.load_checkpoint(bot.last_checkpoint_path)
# unfollow new users
bot.unfollow_users(bot.checkpoint_following_diff(cp))
bot.logout()
