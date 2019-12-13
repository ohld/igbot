"""
    Download a user videos:
    This script could be very useful to download a users videos.

    Dependencies:
        pip install -U instabot
    Run:
      python download_user_videos.py -u username -p password -user user

    Notes:
        You can change file and add there your comments.

    Developed by:
        Steffan Jensen
        http://www.instabotai.com
"""

import os
import sys
import argparse
from instabot import Bot

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-u", type=str, help="username")
parser.add_argument("-p", type=str, help="password")
parser.add_argument("-proxy", type=str, help="proxy")
parser.add_argument("-user", type=str, help="user")
args = parser.parse_args()

# in case if you just downloaded zip with sources
sys.path.append(os.path.join(sys.path[0], "../../"))


bot = Bot()
bot.login(username=args.u, password=args.p, proxy=args.proxy)

user_id = bot.get_user_id_from_username(args.user)
user_medias = bot.get_user_medias(user_id, filtration=None)
for media_id in user_medias:
    bot.api.media_info(media_id)
    json = bot.api.last_json
    media_type = json["items"][0]["media_type"]
    if media_type == 2:
        print("Downloading Video")
        bot.download_video(media_id, folder="videos")
    else:
        print("Not a video")
