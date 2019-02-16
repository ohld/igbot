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

def get_followers_into_file(username,get_what,file_name):
    try:
        user_id = bot.get_user_id_from_username(username)
    except Exception as e:
        bot.logger.error("{}".format(e))
        exit()

    bot.api.get_total_followers_or_followings(user_id=user_id,
                                              which=get_what,
                                              to_file=file_name)

def unfollow_from_bottom():
    #get all following username and unfollow from bottom
    pass


# bot = Bot()
# bot.login(username="bromalayabro", password="subhanallah")

# required arguments
# username = str(input("enter username whose followers or followings you want to get")).strip()
# get_what = str(input("followers or followings")).strip()
# file_name = str(input("file name")).strip()
# get_followers_into_file(username,get_what,file_name)

#while True:
    # loop all task
    #pass

#################################################################################
def like_and_follow(): #file contain username
    with open("vetfolname.txt","r") as f:
        for username in islice(f, 0, 2):
            user_id = username.strip()
            # bot.like_user(user_id, amount=2)
            # bot.follow(user_id)

            print(username)
            print("second",username)


def new_list():
    with open("vetfolname.txt","r") as f:
        lines = f.readlines()
        open("vetfolname.txt", "w").writelines(lines[2:])


# returned_user = like_and_follow()
# print(returned_user)
like_and_follow()
new_list()
like_and_follow()
