#!/usr/bin/env python
import pandas as pd
import datetime, time
import random
import sys, os

sys.path.append(os.path.join(sys.path[0],'../src'))
from core import Instacore
from prepare import get_credentials

def unsubscribe_not_mutually_followers(core):
    """ Unsubscribes from people that don't follow you.
        I know that the name of this exmaple and function is bad.
        Feel free to give me an advice."""
    all_followers_data = core.get_followers(core.user_login)
    followers = [item["username"] for item in all_followers_data][::-1]
    print ("You follow %d people."%len(followers))

    total_unsubscribed = 0
    for follower in followers:
        info = core.get_profile_info(follower)
        time.sleep(5 * random.random())
        if info:
            if not info["follows_viewer"]:
                print ("%s is not following you! Unsubscribe!"%follower)
                if core.unfollow(core.get_user_id_by_username(follower)):
                    total_unsubscribed += 1
                    print ("  Done. Toatal unsubscribed: %d"%total_unsubscribed)
                else:
                    print ("  Something broke up. I can't unsubscribe.")
                time.sleep(30 + 30 * random.random())
        else:
            print ("  Something broke up. I can't get profile info.")

        if total_unsubscribed >= 200:
            print ("You have unsubscribed from 200 people. That's enought. I'll be stopped.")
            break
    print ("Now you follow %d people."%(len(followers) - total_unsubscribed))
    return True

if __name__ == "__main__":
    login, password = get_credentials()
    core = Instacore(login, password)
    unsubscribe_not_mutually_followers(core)
    core.logout()
