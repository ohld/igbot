#!/usr/bin/env python
import pandas as pd
import datetime, time
import random
import sys, os

sys.path.append(os.path.join(sys.path[0],'../'))
from instabot import API

def unfollow_non_followers(api):
    """ Unsubscribes from people that don't follow you.
        I know that the name of this example and function is bad.
        Feel free to give me an advice."""
    print ("Going to unsubcribe from people that are not follow you.")
    all_following_data = api.get_following(api.user_login)
    following = [item["username"] for item in all_following_data][::-1]
    print ("You follow %d people."%len(following))

    total_unsubscribed = 0
    for follower in following:
        info = api.get_profile_info(follower)
        time.sleep(5 * random.random())
        if info:
            if not info["follows_viewer"]:
                print ("%s is not following you! Unsubscribe!"%(follower))
                if api.unfollow(api.get_user_id_by_username(follower)):
                    total_unsubscribed += 1
                    print ("  Done. Total unsubscribed: %d"%(total_unsubscribed))
                else:
                    print ("  Something broke up. I can't unsubscribe.")
                time.sleep(30 + 30 * random.random())
        else:
            print ("  Something broke up. I can't get profile info.")

        if total_unsubscribed >= 200:
            print ("You have unsubscribed from 200 people. That's enought. I'll be stopped.")
            break
    print ("Now you follow %d people."%(len(following) - total_unsubscribed))
    return True

if __name__ == "__main__":
    api = API()
    api.login()
    unfollow_non_followers(api)
    api.logout()
