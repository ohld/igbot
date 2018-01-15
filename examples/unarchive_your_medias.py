"""
    instabot example

    Workflow:
    1) Unarchives your last medias

"""

import os
import sys

from instabot import Bot

sys.path.append(os.path.join(sys.path[0], '../'))

bot = Bot()
bot.login()
medias = bot.get_archived_medias()
bot.unarchive_medias(medias)
