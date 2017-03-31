"""
    instabot example

    Workflow:
        1) unfollows every from your account.
"""

import sys
import os
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

sys.path.append(os.path.join(sys.path[0], '../'))

from instabot import Bot

bot = Bot()
bot.login()
bot.unfollow_everyone()
