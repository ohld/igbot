"""
    ULTIMATE SCRIPT

    It uses data written in files:
        * follow_followers.txt
        * follow_following.txt
        * like_hashtags.txt
        * like_users.txt
    and do the job. This bot can be run 24/7.
"""

import os
import sys

sys.path.append(os.path.join(sys.path[0], "../../"))
from instabot import Bot  # noqa: E402

bot = Bot()
bot.login()

print("Current script's schedule:")
follow_followers_list = bot.read_list_from_file("follow_followers.txt")
print("Going to follow followers of:", follow_followers_list)
follow_following_list = bot.read_list_from_file("follow_following.txt")
print("Going to follow following of:", follow_following_list)
like_hashtags_list = bot.read_list_from_file("like_hashtags.txt")
print("Going to like hashtags:", like_hashtags_list)
like_users_list = bot.read_list_from_file("like_users.txt")
print("Going to like users:", like_users_list)

tasks_list = []
for item in follow_followers_list:
    tasks_list.append((bot.follow_followers, {
        "user_id": item, "nfollows": None
    }))
for item in follow_following_list:
    tasks_list.append((bot.follow_following, {"user_id": item}))
for item in like_hashtags_list:
    tasks_list.append((bot.like_hashtag, {"hashtag": item, "amount": None}))
for item in like_users_list:
    tasks_list.append((bot.like_user, {"user_id": item, "amount": None}))

# shuffle(tasks_list)
for func, arg in tasks_list:
    func(**arg)
