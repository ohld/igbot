import os
import sys
import argparse

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-u", type=str, help="username")
parser.add_argument("-p", type=str, help="password")
parser.add_argument("-proxy", type=str, help="proxy")
parser.add_argument("-location", type=str, help="location")
parser.add_argument("-amount", type=str, help="amount")
args = parser.parse_args()

bot = Bot()
bot.login(username=args.u, password=args.p, proxy=args.proxy)

bot.like_location_feed(args.location, amount=args.amount)
