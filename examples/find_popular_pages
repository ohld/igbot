from instabot import Bot

import imageio

import sys

from collections import Counter

'''
    
    Create List of Users Following a Page

'''

def create_following_list(my_bot,page_name):
    print("Creating List")
    friends = my_bot.get_user_followers(page_name)  # getting following
    friendslist = list(set(friends))  # listing your fiends
    with open("following_{0}.txt".format(my_bot.username), "w") as file:  # writing to the file
        for user_id in friendslist:
            file.write(str(user_id) + "\n")
    print("Task Done")

'''
    
    Create a followers list from a list of userids
    
'''


def create_followers_of_following_list(my_bot,list_of_followers):
    following = open(list_of_followers,'r')
    for follower in following:
        cleanedFollower = follower.strip()
        print cleanedFollower
        username = my_bot.get_username_from_userid(cleanedFollower)
        print username
        usernames = my_bot.get_user_followers(username)
        followerlist = list(set(usernames))
        with open("followers.txt","a") as file:
            for user_id in followerlist:
                file.write(str(user_id) + "\n")
    print("Task Done")

'''
    
    Count repeat userids in a list
    
'''

def find_popular_pages(follower_list):
    with open(follower_list) as f:
        lines = f.read().splitlines()
    count = dict(Counter(lines))
    print count
