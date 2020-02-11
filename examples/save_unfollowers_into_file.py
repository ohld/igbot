"""
    instabot example

    Workflow:
        Save user' unfollowers into a file.
"""
import argparse
import os
import sys

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot, utils  # noqa: E402

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-u", type=str, help="username")
parser.add_argument("-p", type=str, help="password")
parser.add_argument("-proxy", type=str, help="proxy")
args = parser.parse_args()

bot = Bot()
bot.login(username=args.u, password=args.p, proxy=args.proxy)

f = utils.file("config/non-followers.txt")

non_followers = set(bot.following) - set(bot.followers) - bot.friends_file.set
non_followers = list(non_followers)
non_followers_names = []

for user in non_followers:
    name = bot.get_username_from_user_id(user)
    non_followers_names.append(name)
    print(name)
    bot.small_delay()


f.save_list(non_followers_names)
