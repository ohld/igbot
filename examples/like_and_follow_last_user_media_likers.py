"""
    instabot example

    Workflow:
        Like and follow users who liked the last media of input users.
"""

import sys
import os
from tqdm import tqdm
import argparse
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-proxy', type=str, help="proxy")
parser.add_argument('users', type=str, nargs='+', help='users')
args = parser.parse_args()

bot = Bot()
bot.login(username=args.u, password=args.p,
          proxy=args.proxy)

for username in args.users:
    medias = bot.get_user_medias(username, filtration=False)
    if len(medias):
        likers = bot.get_media_likers(medias[0])
        for liker in tqdm(likers):
            bot.like_user(liker, amount=2)
            bot.follow(liker)
