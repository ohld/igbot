"""
    instabot example

    Workflow:
        Download the specified user's medias

"""
import argparse
import os
import sys

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("username", type=str, help="@username")
args = parser.parse_args()

if args.username[0] != "@":  # if first character isn't "@"
    args.username = "@" + args.username

bot = Bot()
bot.login()
medias = bot.get_total_user_medias(args.username)
bot.download_photos(medias)
