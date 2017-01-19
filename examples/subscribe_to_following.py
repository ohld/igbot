#!/usr/bin/env python
import pandas as pd
import datetime, time
import random
import sys, os

sys.path.append(os.path.join(sys.path[0],'../'))
from instabot import API

def subscribe_to_following(api, username):
    """ Subscribes to people that are followed by username. """
    print ("Going to subscribe to persons who are followed by %s"%(username))
    all_following_data = api.get_following(username)
    if len(all_following_data) == 0:
        return True
    followers = [item["username"] for item in all_following_data if item["followed_by_viewer"]][::-1]
    print ("%s follows %d people. You are not follow %d of them."%(username, len(all_following_data), len(followers)))

    total_subscribed = 0
    for follower in followers:
        info = api.get_profile_info(follower)
        if api.follow(api.get_user_id_by_username(follower)):
            total_subscribed += 1
            print ("  Done. Total subscribed: %d"%(total_subscribed))
        else:
            print ("  Something broke up. I can't subscribe to %s"%(follower))
        time.sleep(10 + 10 * random.random())

        if total_subscribed >= 200:
            print ("""You have subscribed to 200 people. That's enought. I'll be stopped.
                      If you want more - just rerun this script. But it isn't safe.""")
            break
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print ("USAGE: python subscribe_to_following.py <username-to-subscribe>")
        exit()
    api = API()
    api.login()
    subscribe_to_following(api, sys.argv[1])
    api.logout()
