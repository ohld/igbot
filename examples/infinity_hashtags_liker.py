"""
    instabot example

    Workflow:
        Like last images with hashtag.
"""

import argparse
import os
import sys
import time

from instabot import Bot

sys.path.append(os.path.join(sys.path[0], "../"))

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-u", type=str, help="username")
parser.add_argument("-p", type=str, help="password")
parser.add_argument("-proxy", type=str, help="proxy")
parser.add_argument("hashtags", type=str, nargs="+", help="hashtags")
args = parser.parse_args()

bot = Bot()
bot.login(username=args.u, password=args.p, proxy=args.proxy)

wait = 5 * 60  # in seconds

while True:
    for hashtag in args.hashtags:
        bot.like_hashtag(hashtag)
    time.sleep(wait)
