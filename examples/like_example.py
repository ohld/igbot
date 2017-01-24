"""
    instabot example

    Workflow:
    1) likes your timeline feed
    2) likes user's feed

    Notes:
    2) You should pass user_id, not username
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
