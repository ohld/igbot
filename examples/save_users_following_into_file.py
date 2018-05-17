"""
    instabot example

    Workflow:
        Save users' following into a file.
"""
import os
import sys
import argparse

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-proxy', type=str, help="proxy")
parser.add_argument('users', type=str, nargs='+', help='users')
args = parser.parse_args()

bot = Bot()
bot.login(username=args.u, password=args.p,
          proxy=args.proxy)

fh = open("users_following.txt", "a+")
for username in args.users:
    following = bot.get_user_following(username)
    for user in following:
        fh.write(user + "\n")
fh.close()
