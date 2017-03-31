"""
    instabot example

    Workflow:
        Like user's, follower's media by user_id.
"""

import sys
import os
import time
import random
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
    bot.like_followers(username, nlikes=3)
