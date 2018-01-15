"""
    instabot example

    Workflow:
        Like rescent medias from your timeline feed.
"""

import os
import sys

from instabot import Bot

sys.path.append(os.path.join(sys.path[0], '../'))


bot = Bot()
bot.login()
bot.like_timeline()
