"""
    instabot example

    Collects the information about your account
    every hour in username.tsv file.
"""

import os
import sys
import time

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

if len(sys.argv) != 2:
    print("USAGE: Pass username to collect stats of - saved in username.tsv (same dir).")
    print("Example: python %s account1" % sys.argv[0])
    exit()

delay = 60 * 60  # in seconds

bot = Bot()
bot.login()
while True:
    bot.save_user_stats(sys.argv[1])
    time.sleep(delay)
