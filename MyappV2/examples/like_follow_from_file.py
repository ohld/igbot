"""
enter username/user id
get all follower in a file

follow each user in the file
like their 3 their pictures
comment on 3 their pictures
unfollow from bottom
"""
import argparse
import os
import sys
import time
import random
from tqdm import tqdm
from itertools import islice

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

# filename = "vetfolname.txt"
bot = Bot()
bot.login(username="bromalayabro", password="subhanallah")

# required arguments from user
username = str(input("enter username whose followers or followings you want to get\n")).strip()
get_what = str(input("followers or followings\n")).strip()
filename = str(input("enter file name.txt \n")).strip()
max_follow_unfollow = int(input("max follow unfollow 100 + random value"))
max_like = int(input("max like 2 + random value"))


#######################################################################################################################

def get_followers_into_file():
    try:
        user_id = bot.get_user_id_from_username(username)
    except Exception as e:
        bot.logger.error("{}".format(e))
        exit()

    bot.api.get_total_followers_or_followings(user_id=user_id,
                                              which=get_what,
                                              to_file=filename,
                                              usernames=True)

def like_and_follow(): #file contain username
    if os.path.getsize(filename):
        with open(filename,"r") as f:
            for username in islice(f, 0, int(100 + max_follow_unfollow * random.random())):
                user_id = username.strip()
                bot.like_user(user_id, amount=int(1 + max_like * random.random()))
                bot.follow(user_id)
                time.sleep(10 + 20 * random.random())
        return True

    else:
        print(filename, "empty")
        return False

def new_list():
    with open(filename,"r") as f:
        lines = f.readlines()
        open(filename, "w").writelines(lines[int(100 + max_follow_unfollow * random.random()):])

#######################################################################################################################

get_followers_into_file()

while like_and_follow():
    like_and_follow()
    new_list()
    bot.unfollow_non_followers(n_to_unfollows=max_follow_unfollow)