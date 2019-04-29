import os
import sys
import argparse

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('username', type=str, help='@username')
parser.add_argument('-story_username', type=str, help='story_username')
args = parser.parse_args()
if args.username[0] != "@":  # if first character isn't "@"
    args.username = "@" + args.username

bot = Bot()
bot.login()

bot.download_stories(args.story_username)
