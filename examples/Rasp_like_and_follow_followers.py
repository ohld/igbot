#python like_user_followers.py -u bromalayabro -p subhanallah -users newkhai.my
"""
get username
get all following
like following
follow following
comment following
"""


import argparse
import os
import sys

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-proxy', type=str, help="proxy")
parser.add_argument('-users', type=str, help='users')
args = parser.parse_args()

bot = Bot()
bot.login(username=args.u, password=args.p,
          proxy=args.proxy)

user_id = bot.get_user_id_from_username(args.users)
followers_list_id = bot.get_user_followers(user_id)

for username in followers_list_id:
    new_user_id = username.strip()
    bot.like_user(new_user_id, amount=3)
    bot.follow(new_user_id)

