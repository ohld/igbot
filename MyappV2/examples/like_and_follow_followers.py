#python like_user_followers.py -u bromalayabro -p subhanallah -users newkhai.my

"""
my script
get username
get all following
like following
follow following
comment following
"""


import argparse
import os
import sys
import time
import random
import schedule
import threading

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot



class like_follow(threading.Thread):
    def run_threaded(self, job_fn):
        job_thread = threading.Thread(target=job_fn)
        job_thread.start()

    def like_and_follow_followers(self):
        followers_list_id = bot.get_user_followers(user_id, nfollows=2000)
        for username in followers_list_id:
            new_user_id = username.strip()
            bot.like_user(new_user_id, amount=2)
            bot.follow(new_user_id)
            time.sleep(30 + 20 * random.random())

    def unfollow_non_followers(self):
        bot.unfollow_non_followers(n_to_unfollows=1000)

    def ignore_error_like_follow(self):
        try:
            self.like_and_follow_followers()
        except:
            self.ignore_error_like_follow()

    def run(self):
        self.run_threaded(self.ignore_error_like_follow)
        schedule.every().day.at("01:30").do(self.run_threaded, self.unfollow_non_followers)

        while True:
            schedule.run_pending()
            time.sleep(1)

###### RUN IN SCRIPT ###########
# bot = Bot()
# # bot.login(username="vicode.co", password="vicode.co98")
# bot.login(username="bromalayabro", password="subhanallah")
# user_id = bot.get_user_id_from_username("neelofa")

###### RUN IN TERMNINAL ######
parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-proxy', type=str, help="proxy")
parser.add_argument('-users', type=str, help='users')
args = parser.parse_args()

bot = Bot()
bot.login(username=args.u, password=args.p,
          proxy=args.proxy)
user_id = bot.get_user_id_from_username(args.users)


like_follow().start()