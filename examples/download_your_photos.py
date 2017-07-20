"""
    instabot example

    Workflow:
    1) Downloads your last medias

"""

import sys
import os

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

bot = Bot()
bot.login()
medias = bot.get_your_medias()
bot.download_photos(medias)
