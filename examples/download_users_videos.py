"""
    Download a user videos:
    This script could be very useful to download many users videos.

    Dependencies:
        pip install -U instabot
    Run:
      python download_users_videos.py -u username -p password -user "user, user2, user3"

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
#sys.path.append(os.path.join(sys.path[0], "../../"))


def convert_usernames_to_list(usernames):
    newlist = []
    ''' convert usernames or hashtags to a list '''
    try:
        for username in usernames.split(", "):
            newlist.append(username)
        list_usernames = newlist

    except:
        for username in usernames.split(","):
            newlist.append(username)
        list_usernames = newlist

    else:
        usernames = list_usernames
    return list_usernames

bot = Bot()
bot.login(username=args.u, password=args.p)

usernames = convert_usernames_to_list(args.user)

for username in usernames:
    user_id = bot.get_user_id_from_username(username)
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
