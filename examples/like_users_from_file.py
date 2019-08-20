"""
    instabot example

    Workflow:
        Take users from input file and like them.
        The file should contain one username per line!
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
parser.add_argument("filepath", type=str, help="filepath")
parser.add_argument("users", type=str, nargs="+", help="users")
args = parser.parse_args()

bot = Bot()
users_to_like = bot.read_list_from_file(args.filepath)
if not users_to_like:
    exit()
else:
    print("Found %d users in file." % len(users_to_like))

bot.login(username=args.u, password=args.p, proxy=args.proxy)

bot.like_users(users_to_like, nlikes=1)
