"""
    instabot example

    Workflow:
        Like and follow you last media likers.
"""

import argparse
import os
import random
import sys
import time

from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot


def like_and_follow(bot, user_id, nlikes=3):
    bot.like_user(user_id, amount=nlikes)
    bot.follow(user_id)
    return True


def like_and_follow_media_likers(bot, media, nlikes=3):
    for user in tqdm(bot.get_media_likers(media), desc="Media likers"):
        like_and_follow(bot, user, nlikes)
        time.sleep(10 + 20 * random.random())
    return True


parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-u", type=str, help="username")
parser.add_argument("-p", type=str, help="password")
parser.add_argument("-proxy", type=str, help="proxy")
parser.add_argument("media_id", type=str, help="media_id")
args = parser.parse_args()

bot = Bot()
bot.login(username=args.u, password=args.p, proxy=args.proxy)

like_and_follow_media_likers(bot, args.media_id)
