"""
    Simple bot usage example which can be used as test for this module.

    Bot
    1) likes your feed
    2) likes user's feed (you should pass user_id, not username)
    3) follows user or list of users
"""

import time
import sys
import os

sys.path.append(os.path.join(sys.path[0],'../'))
from instabot import Bot

bot = Bot()
bot.login()
bot.like_timeline()
bot.like_user_id("352300017")
bot.logout()
