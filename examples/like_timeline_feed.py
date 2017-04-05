"""
    instabot example

    Workflow:
        Like rescent medias from your timeline feed.
"""

import sys
import os

sys.path.append(os.path.join(sys.path[0], '../'))

from instabot import Bot

bot = Bot()
bot.like_timeline()
