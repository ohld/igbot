"""
    instabot example
    Workflow:
        Get total or filtered followers or followings to file.
"""

import argparse
import os
import sys

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot  # noqa: E402

parser = argparse.ArgumentParser(add_help=True)
# login arguments
parser.add_argument("-u", type=str, help="username")
parser.add_argument("-p", type=str, help="password")
parser.add_argument("-proxy", type=str, help="proxy")
# required arguments
parser.add_argument(
    "-user",
    type=str,
    help="username whose followers or followings you want to get",
    required=True,
)
parser.add_argument(
    "-get", type=str, help="followers or followings", required=True
)
parser.add_argument("-file", type=str, help="speficy filename", required=True)
# optional arguments

help_msg = ("set the total amount of followers/followings to check "
            "(if you set filters, returned amount could be less than this)")

parser.add_argument(
    "-amount",
    type=int,
    help=help_msg,
)
parser.add_argument(
    "-overwrite",
    action="store_true",
    help="add this options to overwrite file if exists",
)
parser.add_argument(
    "-usernames",
    action="store_true",
    help="add this options to download usernames instead of user_ids",
)
parser.add_argument(
    "-filter_private",
    action="store_true",
    help="add this options to filter private acccounts",
)
parser.add_argument(
    "-filter_business",
    action="store_true",
    help="add this options to filter business accounts",
)
parser.add_argument(
    "-filter_verified",
    action="store_true",
    help="add this options to filter verified accounts",
)
args = parser.parse_args()

if args.get != "followers" and args.get != "followings":
    print(
        "Wrong option! You can get 'followers' or 'followings'.\n"
        "Type `python get_followers_or_followings_to_file.py "
        "--help` for help and options list"
    )
    exit()

bot = Bot()
bot.login(username=args.u, password=args.p, proxy=args.proxy)

try:
    user_id = bot.get_user_id_from_username(args.user)
except Exception as e:
    bot.logger.error("{}".format(e))
    exit()

bot.api.get_total_followers_or_followings(
    user_id=user_id,
    amount=args.amount,
    which=args.get,
    to_file=args.file,
    overwrite=args.overwrite,
    usernames=args.usernames,
    filter_private=args.filter_private,
    filter_business=args.filter_business,
    filter_verified=args.filter_verified,
)
