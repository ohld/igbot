"""
    instabot example
    Workflow:
    Repost best photos from users to your account
    By default bot checks username_database.txt
    The file should contain one username per line!
"""

import argparse
import os
import sys
import random

from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot, utils  # noqa: E402

USERNAME_DATABASE = "username_database.txt"
POSTED_MEDIAS = "posted_medias.txt"


def repost_best_photos(bot, users, amount=1):
    medias = get_not_used_medias_from_users(bot, users)
    medias = sort_best_medias(bot, medias, amount)
    for media in tqdm(medias, desc="Reposting photos"):
        repost_photo(bot, media)


def sort_best_medias(bot, media_ids, amount=1):
    best_medias = [
        bot.get_media_info(media)[0]
        for media in tqdm(media_ids, desc="Getting media info")
    ]
    best_medias = sorted(
        best_medias, key=lambda x: (x["like_count"], x["comment_count"]), reverse=True
    )
    return [best_media["id"] for best_media in best_medias[:amount]]


def get_not_used_medias_from_users(bot, users=None, users_path=USERNAME_DATABASE):
    if not users:
        if os.stat(USERNAME_DATABASE).st_size == 0:
            bot.logger.warning("No username(s) in thedatabase")
            sys.exit()
        elif os.path.exists(USERNAME_DATABASE):
            users = utils.file(users_path).list
        else:
            bot.logger.warning("No username database")
            sys.exit()

    total_medias = []
    user = random.choice(users)

    medias = bot.get_user_medias(user, filtration=False)
    medias = [media for media in medias if not exists_in_posted_medias(media)]
    total_medias.extend(medias)
    return total_medias


def exists_in_posted_medias(new_media_id, path=POSTED_MEDIAS):
    medias = utils.file(path).list
    return str(new_media_id) in medias


def update_posted_medias(new_media_id, path=POSTED_MEDIAS):
    medias = utils.file(path)
    medias.append(str(new_media_id))
    return True


def repost_photo(bot, new_media_id, path=POSTED_MEDIAS):
    if exists_in_posted_medias(new_media_id, path):
        bot.logger.warning("Media {} was uploaded earlier".format(new_media_id))
        return False
    photo_path = bot.download_photo(new_media_id, save_description=True)
    if not photo_path or not isinstance(photo_path, str):
        # photo_path could be True, False, or a file path.
        return False
    try:
        with open(photo_path[:-3] + "txt", "r") as f:
            text = "".join(f.readlines())
    except FileNotFoundError:
        try:
            with open(photo_path[:-6] + ".txt", "r") as f:
                text = "".join(f.readlines())
        except FileNotFoundError:
            bot.logger.warning("Cannot find the photo that is downloaded")
            pass
    if bot.upload_photo(photo_path, text):
        update_posted_medias(new_media_id, path)
        bot.logger.info("Media_id {} is saved in {}".format(new_media_id, path))
    return True


parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-u", type=str, help="username")
parser.add_argument("-p", type=str, help="password")
parser.add_argument("-proxy", type=str, help="proxy")
parser.add_argument("-file", type=str, help="users filename")
parser.add_argument("-amount", type=int, help="amount", default=1)
parser.add_argument("users", type=str, nargs="*", help="users")
args = parser.parse_args()

bot = Bot()
bot.login(username=args.u, password=args.p, proxy=args.proxy)

users = None
if args.users:
    users = args.users
elif args.file:
    users = utils.file(args.file).list

repost_best_photos(bot, users, args.amount)
