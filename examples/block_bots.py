"""
    instabot example

    Workflow:
        Block bots. That makes them unfollow you -> You have clear account.
"""

import sys
import os
import time
import random
from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

stop_words = ['shop', 'store', 'free']

bot = Bot(stop_words=stop_words)
bot.login()
bot.logger.info("This script will block bots. "
                "So they will no longer be your follower. "
                "Bots are those users who:\n"
                " * follow more than (sample value - change in file) 2000 users\n"
                " * have stopwords in user's info: "
                " %s " % str(stop_words))

your_followers = False
while not your_followers:
    your_followers = bot.get_user_followers(bot.user_id)

your_likers = set()
media_items = bot.get_user_medias(bot.user_id, filtration=False)[:10]
for media_id in tqdm(media_items, desc="Getting your media likers"):
    media_likers = bot.get_media_likers(media_id)
    your_likers |= set(media_likers)

your_followers = list(set(your_followers) - your_likers)
random.shuffle(your_followers)

for user in tqdm(your_followers):
    time.sleep(5)
    if not bot.check_not_bot(user):
        bot.logger.info("Found bot: "
            "https://instagram.com/%s/" % bot.get_user_info(user)["username"])
        bot.block(user)
