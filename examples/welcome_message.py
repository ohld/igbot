"""
    instabot example

    Workflow:
        Welcome message for new followers.
"""

import argparse
import os
import sys

from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

NOTIFIED_USERS_PATH = 'notified_users.txt'

MESSAGE = 'Thank you for a script, sudoguy!'

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-proxy', type=str, help="proxy")
parser.add_argument('-users', type=str, nargs='?', help='a path to already notified users')
parser.add_argument('-message', type=str, nargs='?', help='message text')
args = parser.parse_args()

bot = Bot()
bot.login(username=args.u, password=args.p,
          proxy=args.proxy)

# Use custom message from args if exist
if args.message:
    MESSAGE = args.message

# Check on existed file with notified users
if not bot.check_if_file_exists(NOTIFIED_USERS_PATH):
    followers = bot.get_user_followers(bot.user_id)
    followers = map(str, followers)
    followers_string = '\n'.join(followers)
    with open(NOTIFIED_USERS_PATH, 'w') as users_file:
        users_file.write(followers_string)
    print(
        'All followers saved in file {users_path}.\n'
        'In a next time, for all new followers script will send messages.'.format(
            users_path=NOTIFIED_USERS_PATH
        )
    )
    exit(0)

notified_users = bot.read_list_from_file(NOTIFIED_USERS_PATH)
print('Read saved list of notified users. Count: {count}'.format(
    count=len(notified_users)
))
all_followers = bot.get_user_followers(bot.user_id)
print('Amount of all followers is {count}'.format(
    count=len(all_followers)
))

new_followers = set(all_followers) - set(notified_users)

if not new_followers:
    print('New followers not found')
    exit()

print('Found new followers. Count: {count}'.format(
    count=len(new_followers)
))

new_notified_users = []

for follower in tqdm(new_followers):
    if bot.send_message(MESSAGE, follower):
        new_notified_users.append(follower)

if new_notified_users:
    print('Updating notified users list')
    with open(NOTIFIED_USERS_PATH, 'a') as fo:
        new_notified_users_string = '\n'.join(new_notified_users)
        fo.write('\n{users}'.format(
            users=new_notified_users_string
        ))
