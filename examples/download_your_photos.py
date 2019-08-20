"""
    instabot example

    Workflow:
    1) Downloads your medias

"""

import os
import sys

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot

bot = Bot()
bot.login()
medias = bot.get_total_user_medias(bot.user_id)
bot.download_photos(medias)
