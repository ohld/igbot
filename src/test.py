#!/usr/bin/env python
from core import Instacore
from prepare import check_secret
import time, random

def test():
    while not check_secret():
        pass

    with open("secret.txt", "r") as f:
        login = f.readline().strip()
        password = f.readline().strip()

    core = Instacore(login, password)

    test_media_id = "1338417063622201481"
    test_user_id  = "352300017"
    if core.like(test_media_id).status_code != 200:
        print ("Test failed: Can't like")
        return False
    time.sleep(2 * random.random())
    if core.unlike(test_media_id).status_code != 200:
        print ("Test failed: Can't unlike")
        return False
    time.sleep(2 * random.random())
    if core.follow(test_user_id).status_code != 200:
        print ("Test failed: Can't follow")
        return False
    time.sleep(2 * random.random())
    if core.unfollow(test_user_id).status_code != 200:
        print ("Test failed: Can't unfollow")
        return False
    time.sleep(2 * random.random())
    if core.comment(test_media_id, "Test passed!").status_code != 200:
        print ("Test failed: Can't comment")
        return False
    core.logout()
    return True

if __name__ == "__main__":
    if test():
        print ("All tests have passed!")
