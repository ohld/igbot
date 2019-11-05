"""
    instabot example

    Workflow:
        Like last medias by users.
"""

import argparse
import os
import sys

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot  # noqa: E402

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-u", type=str, help="username")
parser.add_argument("-p", type=str, help="password")
parser.add_argument("-l", type=int, help="limit")
parser.add_argument("-proxy", type=str, help="proxy")
parser.add_argument("users", type=str, nargs="+", help="users")
args = parser.parse_args()

bot = Bot()
bot.login(username=args.u, password=args.p, proxy=args.proxy)

for username in args.users:
    bot.like_user(username, amount=args.l, filtration=False)
