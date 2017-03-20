"""
    instabot example

    Workflow:
        Follow users who post medias with hashtag.
"""

import sys
import os
import time

sys.path.append(os.path.join(sys.path[0], '../'))

from instabot import Bot

if len(sys.argv) < 2:
    print ("USAGE: hash tag / hashtags")
    print ("Example: python %s hashtag1 hashtag2" % sys.argv[0])
    exit()

bot = Bot()
bot.login()

wait = 5 * 60  # in seconds

while True:
    for hashtag in sys.argv[1:]:
        users = bot.get_hashtag_users(hashtag)
        bot.follow_users(users)
	time.sleep(wait)
