from __future__ import unicode_literals

import argparse
import os
import sys
import json
import time

# from tqdm import tqdm

# coding=utf-8
"""
    instabot example

    Workflow:
        If media is NOT commented, comment it with $comment
"""


sys.path.append(os.path.join(sys.path[0], "../../"))
from instabot import Bot  # noqa: E402

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-u", type=str, help="username")
parser.add_argument("-p", type=str, help="password")
parser.add_argument("-proxy", type=str, help="proxy")
parser.add_argument("-user", type=str, help="user", required=True)
parser.add_argument("-comment", type=str, help="comment", required=True)
parser.add_argument("-sleep", type=str, help="default: 2s", required=False)
args = parser.parse_args()

if not args.user:
    print("You need to pass the media user with option\n" "-user TOFOLLOW_USER")
    exit()
if not args.comment:
    print("You need to pass the comment with option\n" "-comment hello")
    exit()

sleep = args.sleep or 2
user = args.user
comment = args.comment

def comment_media_from_user(bot,user,comment):
    # get the latest not-commented media
    print ("Checking medias from user ",user)
    medias = bot.get_user_medias(user,filtration=False,is_comment=False)
    print ("Got ", len(medias), " medias" )
    if len(medias):
        media_id = medias[0]
        # get info
        media_info = bot.get_media_info(media_id)
        media_text = media_info[0]['caption']['text']
        print("Infos: ", media_text)
        # comment it
        bot.comment(int(media_id),comment)
        print("Successfully commented out ",bot.get_link_from_media_id(int(medias[0])))

def run():
    bot = Bot()
    print("Comment: ",comment)
    print("User:    ",user)
    print("Logging...")
    bot.login(username=args.u, password=args.p, proxy=args.proxy)
    while True:
        comment_media_from_user(bot, user, comment)
        print("Sleeping ", str(sleep), "s." )
        time.sleep(sleep)

if __name__ == "__main__":
    run()