# -*- coding: utf-8 -*-
import schedule
import time
import sys
import os
import random
import glob             # ->added to make pics upload -> see job8
import threading        # ->added to make multithreadening possible -> see fn run_threaded

sys.path.append(os.path.join(sys.path[0], '../../'))
from instabot import Bot

import config

bot = Bot(comments_file=config.COMMENTS_FILE, blacklist=config.BLACKLIST_FILE, whitelist=config.WHITELIST_FILE)
bot.login()
bot.logger.info("ULTIMATE script. 24hours save")

random_user_file = bot.read_list_from_file(config.USERS_FILE)
random_hashtag_file = bot.read_list_from_file(config.HASHTAGS_FILE)
photo_captions = bot.read_list_from_file(config.PHOTO_CAPTIONS_FILE)

# to get pics and autopost it
posted_pic_list = []
try:
    with open(config.POSTED_PICS_FILE, 'r') as f:
        posted_pic_list = f.read().splitlines()
except Exception:
    posted_pic_list = []

# Get the filenames of the photos in the path ->
pics = [os.path.basename(x) for x in glob.glob(config.PICS_PATH + "/*.jpg")]
pics = sorted(pics)


# Return a random value from a list, used in various jobs below
def get_random(from_list):
    _random = random.choice(from_list)
    return _random


def stats():
    bot.save_user_stats(bot.user_id)


def job1():
    bot.like_hashtag(get_random(random_hashtag_file), amount=int(700 / 24))


def job2():
    bot.like_timeline(amount=int(300 / 24))


def job3():
    bot.like_followers(get_random(random_user_file), nlikes=3)


def job4():
    bot.follow_followers(get_random(random_user_file), nfollows=config.NUMBER_OF_FOLLOWERS_TO_FOLLOW)


def job5():
    bot.comment_medias(bot.get_timeline_medias())


def job6():
    bot.unfollow_non_followers(n_to_unfollows=config.NUMBER_OF_NON_FOLLOWERS_TO_UNFOLLOW)


def job7():
    bot.follow_users(bot.get_hashtag_users(get_random(random_hashtag_file)))


def job8():  # Comment posts with an hashtag in HASHTAGS_FILE
    hashtag = get_random(random_hashtag_file)
    bot.logger.info("Commenting on hashtag: " + hashtag)
    bot.comment_hashtag(hashtag)


def job9():  # Automatically post a pic in 'pics' folder
    try:
        for pic in pics:
            if pic in posted_pic_list:
                continue

            caption = get_random(photo_captions)
            full_caption = caption + "\n" + config.FOLLOW_MESSAGE
            bot.logger.info("Uploading pic with caption: " + caption)
            bot.uploadPhoto(config.PICS_PATH + pic, caption=full_caption)
            if bot.LastResponse.status_code != 200:
                bot.logger.error("Something went wrong, read the following ->\n")
                bot.logger.error(bot.LastResponse)
                break

            if pic not in posted_pic_list:
                # After posting a pic, comment it with all the hashtags specified
                # In config.PICS_HASHTAGS
                posted_pic_list.append(pic)
                with open('pics.txt', 'a') as f:
                    f.write(pic + "\n")
                bot.logger.info("Succesfully uploaded: " + pic)
                bot.logger.info("Commenting uploaded photo with hashtags...")
                medias = bot.get_your_medias()
                last_photo = medias[0]  # Get the last photo posted
                bot.comment(last_photo, config.PICS_HASHTAGS)
                break
    except Exception as e:
        bot.logger.error("Couldn't upload pic")
        bot.logger.error(str(e))


def job10():  # put non followers on blacklist
    try:
        bot.logger.info("Creating non-followers list")
        followings = bot.get_user_following(bot.user_id)  # getting following
        followers = bot.get_user_followers(bot.user_id)  # getting followers
        friends_file = bot.read_list_from_file("friends.txt")  # same whitelist (just user ids)
        nonfollowerslist = list((set(followings) - set(followers)) - set(friends_file))
        with open(config.BLACKLIST_FILE, 'a') as file:  # writing to the blacklist
            for user_id in nonfollowerslist:
                file.write(str(user_id) + "\n")
        bot.logger.info("Removing duplicates...")
        lines = open(config.BLACKLIST_FILE, 'r').readlines()
        lines_set = set(lines)
        out = open(config.BLACKLIST_FILE, 'w')
        for line in lines_set:
            out.write(line)
        bot.logger.info("Done.")
    except Exception as e:
        bot.logger.error("Couldn't update blacklist")
        bot.logger.error(str(e))


# function to make threads -> details here http://bit.ly/faq_schedule
def run_threaded(job_fn):
    job_thread = threading.Thread(target=job_fn)
    job_thread.start()


schedule.every(1).hour.do(run_threaded, stats)              # get stats
schedule.every(8).hours.do(run_threaded, job1)              # like hashtag
schedule.every(2).hours.do(run_threaded, job2)              # like timeline
schedule.every(1).days.at("16:00").do(run_threaded, job3)   # like followers of users from file
schedule.every(2).days.at("11:00").do(run_threaded, job4)   # follow followers
schedule.every(16).hours.do(run_threaded, job5)             # comment medias
schedule.every(1).days.at("08:00").do(run_threaded, job6)   # unfollow non-followers
schedule.every(12).hours.do(run_threaded, job7)             # follow users from hashtag from file
schedule.every(6).hours.do(run_threaded, job8)              # comment hashtag
schedule.every(1).days.at("21:28").do(run_threaded, job9)   # upload pics
schedule.every(4).days.at("07:50").do(run_threaded, job10)  # non-followers blacklist

while True:
    schedule.run_pending()
    time.sleep(1)
