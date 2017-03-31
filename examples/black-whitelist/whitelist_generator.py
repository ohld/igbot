"""
    instabot example

    Whitelist generator: generates a list of users which
    will not be unfollowed.
"""

import sys
import os
import random
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

sys.path.append(os.path.join(sys.path[0], '../../'))
from instabot import Bot

bot = Bot()
bot.login()

print ("This script will generate whitelist.txt file with users"
       "who will not be unfollowed by bot. "
       "Press Y to add user to whitelist. Ctrl + C to exit.")
your_following = bot.get_user_following(bot.user_id)
already_whitelisted = bot.read_list_from_file("whitelist.txt")
rest_users = list(set(your_following) - set(already_whitelisted))
random.shuffle(rest_users)
with open("whitelist.txt", "a") as f:
    for user_id in rest_users:
        user_info = bot.get_user_info(user_id)
        print(user_info["username"])
        print(user_info["full_name"])

        input_line = sys.stdin.readline().lower()
        if "y" in input_line:
            f.write(str(user_id) + "\n")
            print("ADDED.\r")
