"""
    instabot example

    Workflow:
        1) unfollows every from your account.
"""

import sys
import os

sys.path.append(os.path.join(sys.path[0], '../'))

from instabot import Bot

bot = Bot()
bot.login()
bot.unfollow_everyone()
