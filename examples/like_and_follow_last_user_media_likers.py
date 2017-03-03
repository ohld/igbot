"""
    instabot example

    Workflow:
        Like and follow users who liked the last media of input users.
"""

import sys
import os
from tqdm import tqdm
sys.path.append(os.path.join(sys.path[0],'../'))

from instabot import Bot

if len(sys.argv) < 2:
    print ("USAGE: Pass username / usernames.")
    print ("Example: python %s ohld lenakolenka" % sys.argv[0])
    exit()

bot = Bot()
bot.login()

for username in sys.argv[1:]:
    medias = bot.get_user_medias(username, filtration=False)
    if len(medias):
        likers = bot.get_media_likers(medias[0])
        for liker in tqdm(likers):
            bot.like_user(liker, amount=2)
            bot.follow(liker)
