"""
    instabot example

    Workflow:
        Archive medias.
"""

import argparse
import os
import sys

from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot


def archive_medias(bot, medias):
    for media in tqdm(medias, desc="Medias"):
        bot.archive(media)
    return True


parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-u", type=str, help="username")
parser.add_argument("-p", type=str, help="password")
parser.add_argument("-proxy", type=str, help="proxy")
parser.add_argument("media_id", type=str, nargs="+", help="media_id")
args = parser.parse_args()

bot = Bot()
bot.login(username=args.u, password=args.p, proxy=args.proxy)

archive_medias(bot, args.media_id)
