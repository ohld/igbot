import schedule
import time
import sys
import os
import random
import yaml             #->added to make pics upload -> see job8
import glob             #->added to make pics upload -> see job8
from tqdm import tqdm
import threading        #->added to make multithreadening possible -> see fn run_threaded

sys.path.append(os.path.join(sys.path[0],'../../'))
from instabot import Bot

bot = Bot(comments_file="comments.txt")
bot.login()
bot.logger.info("ULTIMATE script. 24hours save")

comments_file_name = "comments.txt"
random_user_file = bot.read_list_from_file("username_database.txt")
random_hashtag_file = bot.read_list_from_file("hashtag_database.txt")

#to get pics and autopost it
posted_pic_list = []
try:
    with open('pics.txt', 'r') as f:
        posted_pic_list = f.read().splitlines()
except:
    posted_pic_list = []
#!!-> to work this feature properly write full/absolute path to .jgp files as follows ->v
pics = glob.glob("/home/user/instagram/instabot/examples/ultimate_schedule/pics/*.jpg")  #!!change this
pics = sorted(pics)
#end of pics processing

#fn to return random value for separate jobs
def get_random(from_list):
    _random=random.choice(from_list)
    print("Random from ultimate.py script is chosen: \n" + _random + "\n")
    return _random

def job1(): bot.like_hashtag(get_random(random_hashtag_file), amount=int(700/24))
def job2(): bot.like_timeline(amount=int(300/24))
def job3(): bot.like_followers(get_random(random_user_file), nlikes=3)
def job4(): bot.follow_followers(get_random(random_user_file))
def job5(): bot.comment_medias(bot.get_timeline_medias())
def job6(): bot.unfollow_non_followers()
def job7(): bot.follow_users(bot.get_hashtag_users(get_random(random_hashtag_file)))
def job8(): #-->fn to upload photos /auto_uploader
    try:
        for pic in pics:
            if pic in posted_pic_list:
                continue
            hashtags = "/>\n​​#instabot #vaskokorobko #kyiv"       #add custom hashtags
            caption = pic[:-4].split(" ")                        #caption is made from the name of file
            caption = " ".join(caption[1:])
            caption = "\n<" + caption + hashtags                 #create full caption with hashtags
            print("upload: " + caption)
            bot.uploadPhoto(pic, caption=caption)
            if bot.LastResponse.status_code != 200:
                print("Smth went wrong. Read the following ->\n")
                print(bot.LastResponse)
                # snd msg
                break

            if not pic in posted_pic_list:
                posted_pic_list.append(pic)
                with open('pics.txt', 'a') as f:
                    f.write(pic + "\n")
                print("Succsesfully uploaded: " + pic)
                break
    except Exception as e:
        print(str(e))
#end of job8

#function to make threads -> details here http://bit.ly/faq_schedule
def run_threaded(job_fn):
    job_thread=threading.Thread(target=job_fn)
    job_thread.start()

schedule.every(8).hours.do(run_threaded, job1)              #like hashtag
schedule.every(2).hours.do(run_threaded, job2)              #like timeline
schedule.every(1).days.at("16:00").do(run_threaded, job3)   #like followers of users from file
schedule.every(2).days.at("11:00").do(run_threaded, job4)   #follow followers
schedule.every(16).hours.do(run_threaded, job5)             #comment medias
schedule.every(1).days.at("08:00").do(run_threaded, job6)   #unfollow non-followers
schedule.every(12).hours.do(run_threaded, job7)             #follow users from hashtag from file
schedule.every(1).days.at("21:28").do(run_threaded, job8)   #upload pics

while True:
    schedule.run_pending()
    time.sleep(1)
