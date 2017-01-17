#!/usr/bin/env python
import time, random, sys, os

sys.path.append(os.path.join(sys.path[0],'../../'))
from instabot import API
from prepare import check_secret

def test():

    core = API()
    if not core.login_status:
        print ("Test failed: Can't login.")
        return False

    test_media_id = "1338417063622201481"
    test_user_id  = "352300017"
    if not core.like(test_media_id):
        print ("Test failed: Can't like")
        return False
    time.sleep(2 * random.random())

    if not core.unlike(test_media_id):
        print ("Test failed: Can't unlike")
        return False
    time.sleep(2 * random.random())

    if not core.follow(test_user_id):
        print ("Test failed: Can't follow")
        return False
    time.sleep(2 * random.random())

    if not core.unfollow(test_user_id):
        print ("Test failed: Can't unfollow")
        return False
    time.sleep(2 * random.random())

    if not core.comment(test_media_id, "Test passed!"):
        print ("Test failed: Can't comment")
        return False
    core.logout()
    return True

if __name__ == "__main__":
    if test():
        print ("All tests have passed!")
