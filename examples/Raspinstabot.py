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

filename = "vetfolname.txt"

def get_followers_into_file(username,get_what,file_name = filename):
    try:
        user_id = bot.get_user_id_from_username(username)
    except Exception as e:
        bot.logger.error("{}".format(e))
        exit()

    bot.api.get_total_followers_or_followings(user_id=user_id,
                                              which=get_what,
                                              to_file=file_name)

def like_and_follow(max_follow_unfollow,max_like): #file contain username
    if os.path.getsize(filename):
        with open(filename,"r") as f:
            for username in islice(f, 0, max_follow_unfollow):
                user_id = username.strip()
                bot.like_user(user_id, amount=max_like)
                bot.follow(user_id)
                time.sleep(10 + 20 * random.random())

    else:
        print(filename, "empty")

def new_list(max_follow_unfollow):
    with open(filename,"r") as f:
        lines = f.readlines()
        open(filename, "w").writelines(lines[max_follow_unfollow:])





# bot = Bot()
# bot.login(username="bromalayabro", password="subhanallah")

# required arguments from user
# username = str(input("enter username whose followers or followings you want to get")).strip()
# get_what = str(input("followers or followings")).strip()
# file_name = str(input("file name")).strip()
max_follow_unfollow = int(100 + int(input ("max follow unfollow 100 + random value"))* random.random())
max_like = int(2 + int(input ("max like 2 + random value"))* random.random())


# get_followers_into_file(username,get_what,file_name)
# like_and_follow()
# new_list()
# bot.unfollow_non_followers(n_to_unfollows=value)

#while True:
    # loop all task
    #pass
