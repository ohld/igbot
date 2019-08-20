import os
import sys
import argparse

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-u", type=str, help="username")
parser.add_argument("-p", type=str, help="password")
parser.add_argument("-proxy", type=str, help="proxy")
parser.add_argument("-story_username", type=str, help="story_username")
args = parser.parse_args()

bot = Bot()
bot.login(username=args.u, password=args.p, proxy=args.proxy)

# (The following functions apply if you have a private account)

# Approve users that requested to follow you
bot.approve_pending_follow_requests()

# Reject users that requested to follow you
bot.reject_pending_follow_requests()
