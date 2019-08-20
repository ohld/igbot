"""
    instabot example

    Workflow:
        Like rescent medias from your timeline feed.
"""

import os
import sys

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot


bot = Bot()
bot.login()
bot.like_timeline()
