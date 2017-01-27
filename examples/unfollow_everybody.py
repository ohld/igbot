"""
    instabot example

    Workflow:
    1) get list of your followings
    2) unsubscribe from everyone
"""

import sys
import os

sys.path.append(os.path.join(sys.path[0],'../'))
from instabot import Bot

bot = Bot()
bot.login()
following = [item["pk"] for item in bot.getTotalSelfFollowings()]
bot.unfollow_users(following)
bot.logout()
