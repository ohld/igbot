"""
    instabot example

    Workflow:
        Block bots. That makes them unfollow you -> You have clear account.
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
args = parser.parse_args()


stop_words = ["shop", "store", "free"]
bot = Bot(stop_words=stop_words)
bot.login(username=args.u, password=args.p, proxy=args.proxy)

bot.logger.info(
    "This script will block bots. "
    "So they will no longer be your follower. "
    "Bots are those users who:\n"
    " * follow more than (sample value - change in file) 2000 users\n"
    " * have stopwords in user's info: "
    " %s " % str(stop_words)
)
bot.block_bots()
