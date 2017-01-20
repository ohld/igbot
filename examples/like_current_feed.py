#!/usr/bin/env python
import datetime, time
import random
import sys, os

sys.path.append(os.path.join(sys.path[0],'../'))
from instabot import API

def like_current_feed(api, amount):
    """ Subscribes to people that are followed by username. """
    print ("Going to like %d medias of your feed."%(amount))
    all_feed = api.get_feed(amount)
    not_liked_feed = [item["id"] for item in all_feed if not item["likes"]["viewer_has_liked"]]
    print ("  Recieved %d of your last feed. You have already liked %d on them."%\
                            (len(all_feed), len(all_feed) - len(not_liked_feed)))

    total_liked = 0
    for media in not_liked_feed:
        if total_liked % 10 == 0:
            print ("  Total liked: %d"%(total_liked))
        if api.like(media):
            total_liked += 1
        else:
            print ("  Something broke up. I can't like %s"%(media))
        time.sleep(5 + 10 * random.random())

        if total_liked >= 1000:
            print ("""You have liked 1000 media. That's enought. I'll be stopped.
                      If you want more - just rerun this script. But it isn't safe.""")
            break
    print ("      DONE: Total liked: %d"%(total_liked))
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print ("USAGE: python like_current_feed.py <amount of feed to like>")
        exit()
    if not sys.argv[1].isdigit():
        print (" You should pass a number.")
        exit()

    api = API()
    api.login()
    like_current_feed(api, int(sys.argv[1]))
    api.logout()
