"""
    instabot example

    Workflow:
        Follow user's followers by username.
"""

import argparse
import os
import sys

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

# parser = argparse.ArgumentParser(add_help=True)
# parser.add_argument('-u', type=str, help="username")
# parser.add_argument('-p', type=str, help="password")
# parser.add_argument('-proxy', type=str, help="proxy")
# parser.add_argument('users', type=str, nargs='+', help='users')
# args = parser.parse_args()

bot = Bot()
bot.login(username="vicode.co", password="vicode.co98")
username = "bromalayabro"

bot.follow_followers(username,nfollows=50)
