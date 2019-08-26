"""
    instabot example

    Send photo to user
"""

import argparse
import os
import sys

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot  # noqa: E402

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-u", type=str, help="username")
parser.add_argument("-p", type=str, help="password")
parser.add_argument("user", type=str, nargs="*", help="user")
parser.add_argument("--filepath", required=True)
args = parser.parse_args()

bot = Bot()
bot.login(username=args.u, password=args.p)
bot.send_photo(args.user, args.filepath)
