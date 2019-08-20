"""
    instabot example

    Workflow:
        Like last images with hashtags from file.
"""

import argparse
import os
import sys

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-u", type=str, help="username")
parser.add_argument("-p", type=str, help="password")
parser.add_argument("-proxy", type=str, help="proxy")
parser.add_argument("filename", type=str, help="filename")
args = parser.parse_args()

bot = Bot()
bot.login(username=args.u, password=args.p, proxy=args.proxy)

hashtags = bot.read_list_from_file(args.filename)
bot.logger.info("Hashtags: " + str(hashtags))
if not hashtags:
    exit()

bot.login()
for hashtag in hashtags:
    bot.like_hashtag(hashtag)
