import time
import sys
import os
import glob

sys.path.append(os.path.join(sys.path[0], '../../'))
from instabot import Bot

posted_pic_list = []
try:
    with open('pics.txt', 'r') as f:
        posted_pic_list = f.read().splitlines()
except Exception:
    posted_pic_list = []

timeout = 24 * 60 * 60  # pics will be posted every 24 hours

bot = Bot()
bot.login()

while True:
    pics = glob.glob("./pics/*.jpg")
    pics = sorted(pics)
    try:
        for pic in pics:
            if pic in posted_pic_list:
                continue

            caption = pic[:-4].split(" ")
            caption = " ".join(caption[1:])

            print("upload: " + caption)
            bot.uploadPhoto(pic, caption=caption)
            if bot.LastResponse.status_code != 200:
                print(bot.LastResponse)
                # snd msg
                break

            if pic not in posted_pic_list:
                posted_pic_list.append(pic)
                with open('pics.txt', 'a') as f:
                    f.write(pic + "\n")

            time.sleep(timeout)

    except Exception as e:
        print(str(e))
    time.sleep(60)
