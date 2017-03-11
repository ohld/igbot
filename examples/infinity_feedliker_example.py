"""
    instabot example

    Workflow:
        Like rescent medias from your timeline feed.
"""

import sys
import os
import time 

sys.path.append(os.path.join(sys.path[0], '../'))

from instabot import Bot

bot = Bot()
bot.login()

while True:
	bot.like_timeline()
	time.sleep(1*60)
