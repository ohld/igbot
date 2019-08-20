"""
    instabot example

    Collects the information about your account
    every hour in username.tsv file.
"""

import argparse
import os
import sys
import time

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-u", type=str, help="username")
parser.add_argument("-p", type=str, help="password")
parser.add_argument("-proxy", type=str, help="proxy")
parser.add_argument("user", type=str, nargs="*", help="user")
parser.add_argument("-path", type=str, default="", help="path")
args = parser.parse_args()

bot = Bot()
bot.login(username=args.u, password=args.p, proxy=args.proxy)

delay = 60 * 60

while True:
    bot.save_user_stats(args.user, path=args.path)
    time.sleep(delay)
