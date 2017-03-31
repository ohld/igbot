"""
    instabot example

    Workflow:
        1) Reads user_ids from blacklist and whitelist
        2) likes several last medias by users in your timeline

    Notes:
        blacklist and whitelist files should contain user_ids - each one on the
        separate line.
        Example:
            1234125
            1234124512
"""

import sys
import os
from tqdm import tqdm
import argparse
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

sys.path.append(os.path.join(sys.path[0], '../../'))
from instabot import Bot

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-proxy', type=str, help="proxy")
args = parser.parse_args()

bot = Bot(whitelist="whitelist.txt",
          blacklist="blacklist.txt")

bot.login(username=args.u, password=args.p,
          proxy=args.proxy)

timeline_medias = bot.get_timeline_medias()
for media in tqdm(timeline_medias, desc="timeline"):
    bot.like_user(bot.get_media_owner(media))
