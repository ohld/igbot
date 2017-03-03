"""
    instabot example

    Workflow:
    1) likes your timeline feed
    2) likes user's feed

    Notes:
    2) You should pass user_id, not username
"""

import time
import sys
import os

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

bot = Bot()
bot.login()

# like media by a single user_id
bot.like_user("352300017")

# likes all media from timeline
bot.like_timeline()

# likes all media from timeline
bot.like_medias(bot.get_timeline_medias())

# likes media by hashtag(s)
tags = ["l4l", "selfie"]

for t in tags:
    bot.like_hashtag(t)
