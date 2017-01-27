"""
    instabot example

    Workflow:
        1) creates checkpoint: saves your current followings
        2) like and follow likers of last medias from your timeline feed.
        3) reverts to checkpoint: unfollow new followings.
"""

import sys
import os
import time
import random
from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0],'../'))
from instabot import Bot

bot = Bot()
bot.login()
bot.save_checkpoint()
timeline_medias = bot.get_timeline_medias()
for media in tqdm(timeline_medias, desc="timeline"):
    bot.like_and_follow_media_likers(media)
cp = bot.load_last_checkpoint()
bot.revert_to_checkpoint(cp)
bot.logout()
