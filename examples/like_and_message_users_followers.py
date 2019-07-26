"""
    instabot example
    Workflow:
        Send new DM to specified user's followers every X minutes/hours and like their medias
"""

import argparse
import os
import sys
import random
import time
import schedule
sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot, utils

bot = Bot(filter_users=False,)
bot.login()
messagesToSend = 100
banDelay = (86400 / messagesToSend)
user = input("what user's followers to scrape?: ")
a = ["hey", "hello i love your page", "you look good", "whatsup" , "you good" , "boop", "great", "you have a lovely profile" ]
def message():
    followers = bot.get_user_followers(user,3)
    for media in followers:
        bot.get_user_medias(media)
        time.sleep(10)
        bot.like_user(media,amount=2)
    bot.send_messages(random.choice(a),followers)
    print('Waiting ' + str(banDelay) + ' seconds...')
    time.sleep(banDelay)
message()
schedule.every(20).minutes.do(message)
while True:
    schedule.run_pending()
