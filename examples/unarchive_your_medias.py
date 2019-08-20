"""
    instabot example

    Workflow:
    1) Unarchives your last medias

"""

import os
import sys

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot

bot = Bot()
bot.login()
medias = bot.get_archived_medias()
bot.unarchive_medias(medias)
