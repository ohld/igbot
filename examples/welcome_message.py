"""
instabot example
Workflow:
Welcome message for new followers.
"""
import argparse
import os
import sys

from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot, utils  # noqa: E402

NOTIFIED_USERS_PATH = "notified_users.txt"
MESSAGE = "Hi, thanks for reaching me"
parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-u", type=str, help="username")
parser.add_argument("-p", type=str, help="password")
parser.add_argument("-proxy", type=str, help="proxy")
parser.add_argument(
    "-users", type=str, nargs="?", help="a path to already notified users"
)
parser.add_argument("-message", type=str, nargs="?", help="message text")
args = parser.parse_args()
bot = Bot()
bot.login(username=args.u, password=args.p, proxy=args.proxy)
followers = bot.get_user_followers(args.u)
# Use custom message from args if exist
if args.message:
    MESSAGE = args.message
# Check on existed file with notified users
notified_users = utils.file(NOTIFIED_USERS_PATH)
if not notified_users.list:
    notified_users.save_list(followers)
    print(
        (
            "All followers saved in file {users_path}.\n"
            "In a next time, for all new followers "
            "script will send messages."
        ).format(
            users_path=NOTIFIED_USERS_PATH
        )
    )
    exit(0)
print(
    "Read saved list of notified users. Count: {count}".format(
        count=len(notified_users)
    )
)
all_followers = followers
print("Amount of all followers is {count}".format(count=len(all_followers)))
new_followers = set(all_followers) - notified_users.set
if not new_followers:
    print("New followers not found")
    exit()
print("Found new followers. Count: {count}".format(count=len(new_followers)))
for follower in tqdm(new_followers):
    if bot.send_message(MESSAGE, follower):
        notified_users.append(follower)
