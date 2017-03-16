import schedule
import time
import sys
import os
import random
from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0],'../../'))
from instabot import Bot

bot = Bot()
bot.login()
bot.logger.info("ULTIMATE script. 24hours save")

comments_file_name = "comments.txt"
random_user_file = bot.read_list_from_file("username_database.txt")
random_user=random.choice(random_user_file)
random_hashtag_file = bot.read_list_from_file("hashtag_database.txt")
random_hashtag=random.choice(random_hashtag_file)

def job1(): bot.like_hashtag(random_hashtag, amount=int(700/24))
def job2(): bot.like_timeline(amount=int(300/24))
def job3(): bot.like_followers(random_user, nlikes=3)
def job4(): bot.follow_followers(random_user)
def job5(): bot.comment_medias(bot.get_timeline_medias())
def job6(): bot.unfollow_non_followers()

schedule.every(1).hours.do(job1)
schedule.every(1).hours.do(job2)
schedule.every(1).days.at("16:00").do(job3)
schedule.every(1).days.at("11:00").do(job4)
schedule.every(2).hours.do(job5)
schedule.every(1).days.at("08:00").do(job6)

while True:
    schedule.run_pending()
    time.sleep(1)
