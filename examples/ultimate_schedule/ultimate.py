# -*- coding: utf-8 -*-

import os
import sys
import threading
import time
from glob import glob

import config

sys.path.append(os.path.join(sys.path[0], "../../"))
import schedule  # noqa: E402
from instabot import Bot, utils  # noqa: E402


bot = Bot(
    comments_file=config.COMMENTS_FILE,
    blacklist_file=config.BLACKLIST_FILE,
    whitelist_file=config.WHITELIST_FILE,
    friends_file=config.FRIENDS_FILE,
)
bot.login()
bot.logger.info("ULTIMATE script. Safe to run 24/7!")

random_user_file = utils.file(config.USERS_FILE)
random_hashtag_file = utils.file(config.HASHTAGS_FILE)
photo_captions_file = utils.file(config.PHOTO_CAPTIONS_FILE)
posted_pic_list = utils.file(config.POSTED_PICS_FILE).list

pics = sorted([
    os.path.basename(x) for x in glob(config.PICS_PATH + "/*.jpg")
])


def stats():
    bot.save_user_stats(bot.user_id)


def like_hashtags():
    bot.like_hashtag(
        random_hashtag_file.random(), amount=700 // 24
    )


def like_timeline():
    bot.like_timeline(amount=300 // 24)


def like_followers_from_random_user_file():
    bot.like_followers(random_user_file.random(), nlikes=3)


def follow_followers():
    bot.follow_followers(
        random_user_file.random(),
        nfollows=config.NUMBER_OF_FOLLOWERS_TO_FOLLOW
    )


def comment_medias():
    bot.comment_medias(bot.get_timeline_medias())


def unfollow_non_followers():
    bot.unfollow_non_followers(
        n_to_unfollows=config.NUMBER_OF_NON_FOLLOWERS_TO_UNFOLLOW
    )


def follow_users_from_hashtag_file():
    bot.follow_users(bot.get_hashtag_users(random_hashtag_file.random()))


def comment_hashtag():
    hashtag = random_hashtag_file.random()
    bot.logger.info("Commenting on hashtag: " + hashtag)
    bot.comment_hashtag(hashtag)


def upload_pictures():  # Automatically post a pic in 'pics' folder
    try:
        for pic in pics:
            if pic in posted_pic_list:
                continue

            caption = photo_captions_file.random()
            full_caption = caption + "\n" + config.FOLLOW_MESSAGE
            bot.logger.info("Uploading pic with caption: " + caption)
            bot.upload_photo(config.PICS_PATH + pic, caption=full_caption)
            if bot.api.last_response.status_code != 200:
                bot.logger.error(
                    "Something went wrong, read the following ->\n"
                )
                bot.logger.error(bot.api.last_response)
                break

            if pic not in posted_pic_list:
                # After posting a pic, comment it with all the
                # hashtags specified in config.PICS_HASHTAGS
                posted_pic_list.append(pic)
                with open("pics.txt", "a") as f:
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


def put_non_followers_on_blacklist():  # put non followers on blacklist
    try:
        bot.logger.info("Creating non-followers list")
        followings = set(bot.following)
        followers = set(bot.followers)
        friends = bot.friends_file.set  # same whitelist (just user ids)
        non_followers = followings - followers - friends
        for user_id in non_followers:
            bot.blacklist_file.append(user_id, allow_duplicates=False)
        bot.logger.info("Done.")
    except Exception as e:
        bot.logger.error("Couldn't update blacklist")
        bot.logger.error(str(e))


def run_threaded(job_fn):
    job_thread = threading.Thread(target=job_fn)
    job_thread.start()


schedule.every(1).hour.do(run_threaded, stats)
schedule.every(8).hours.do(run_threaded, like_hashtags)
schedule.every(2).hours.do(run_threaded, like_timeline)
schedule.every(1).days.at("16:00").do(
    run_threaded, like_followers_from_random_user_file
)
schedule.every(2).days.at("11:00").do(run_threaded, follow_followers)
schedule.every(16).hours.do(run_threaded, comment_medias)
schedule.every(1).days.at("08:00").do(run_threaded, unfollow_non_followers)
schedule.every(12).hours.do(run_threaded, follow_users_from_hashtag_file)
schedule.every(6).hours.do(run_threaded, comment_hashtag)
schedule.every(1).days.at("21:28").do(run_threaded, upload_pictures)
schedule.every(4).days.at("07:50").do(
    run_threaded, put_non_followers_on_blacklist
)

while True:
    schedule.run_pending()
    time.sleep(1)
