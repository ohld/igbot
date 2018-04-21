# -*- coding: utf-8 -*-

from glob import glob
import os
import random
import sys
import threading
import time

sys.path.append(os.path.join(sys.path[0], '../../'))
import schedule
from instabot import Bot

import config

bot = Bot(comments_file=config.COMMENTS_FILE,
          blacklist_file=config.BLACKLIST_FILE,
          whitelist_file=config.WHITELIST_FILE,
          friends_file=config.FRIENDS_FILE)
bot.login()
bot.logger.info("ULTIMATE script. 24hours save")

random_user_file = instabot.utils.file(config.USERS_FILE)
random_hashtag_file = instabot.utils.file(config.HASHTAGS_FILE)
photo_captions_file = instabot.utils.file(config.PHOTO_CAPTIONS_FILE)
posted_pic_list = instabot.utils.file(config.POSTED_PICS_FILE).list

# Get the filenames of the photos in the path ->
pics = [os.path.basename(x) for x in glob(config.PICS_PATH + "/*.jpg")]
pics = sorted(pics)


def stats():
    bot.save_user_stats(bot.user_id)


def job1():
    bot.like_hashtag(random_hashtag_file.random(), amount=int(700 / 24))


def job2():
    bot.like_timeline(amount=int(300 / 24))


def job3():
    bot.like_followers(random_user_file.random(), nlikes=3)


def job4():
    bot.follow_followers(random_user_file.random(), nfollows=config.NUMBER_OF_FOLLOWERS_TO_FOLLOW)


def job5():
    bot.comment_medias(bot.get_timeline_medias())


def job6():
    bot.unfollow_non_followers(n_to_unfollows=config.NUMBER_OF_NON_FOLLOWERS_TO_UNFOLLOW)


def job7():
    bot.follow_users(bot.get_hashtag_users(random_hashtag_file.random()))


def job8():  # Comment posts with an hashtag in HASHTAGS_FILE
    hashtag = random_hashtag_file.random()
    bot.logger.info("Commenting on hashtag: " + hashtag)
    bot.comment_hashtag(hashtag)


def job9():  # Automatically post a pic in 'pics' folder
    try:
        for pic in pics:
            if pic in posted_pic_list:
                continue

            caption = photo_captions_file.random()
            full_caption = caption + "\n" + config.FOLLOW_MESSAGE
            bot.logger.info("Uploading pic with caption: " + caption)
            bot.upload_photo(config.PICS_PATH + pic, caption=full_caption)
            if bot.last_response.status_code != 200:
                bot.logger.error("Something went wrong, read the following ->\n")
                bot.logger.error(bot.last_response)
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
        followings = set(bot.following)  # getting following
        followers = set(bot.followers)  # getting followers
        friends = bot.friends_file.set  # same whitelist (just user ids)
        non_followers = followings - followers - friends
        for user_id in non_followers:
            bot.blacklist_file.append(user_id, allow_duplicates=False)
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
