from __future__ import unicode_literals

import argparse
import os
import sys

import captions_for_medias

sys.path.append(os.path.join(sys.path[0], "../../"))
from instabot import Bot  # noqa: E402


parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-u", type=str, help="username")
parser.add_argument("-p", type=str, help="password")
parser.add_argument("-proxy", type=str, help="proxy")
parser.add_argument("-photo", type=str, help="photo name")
parser.add_argument("-caption", type=str, help="caption for photo")
args = parser.parse_args()

bot = Bot()
bot.login()

posted_pic_file = "pics.txt"

posted_pic_list = []
caption = ""

if not os.path.isfile(posted_pic_file):
    with open(posted_pic_file, "w"):
        pass
else:
    with open(posted_pic_file, "r") as f:
        posted_pic_list = f.read().splitlines()

# Get the filenames of the photos in the path ->
if not args.photo:
    import glob

    pics = []
    exts = ["jpg", "JPG", "jpeg", "JPEG", "png", "PNG"]
    for ext in exts:
        pics += [
            os.path.basename(x) for x in glob.glob("media/*.{}".format(ext))
        ]
    from random import shuffle

    shuffle(pics)
else:
    pics = [args.photo]
pics = list(set(pics) - set(posted_pic_list))
if len(pics) == 0:
    if not args.photo:
        bot.logger.warn("NO MORE PHOTO TO UPLOAD")
        exit()
    else:
        bot.logger.error("The photo `{}` has already been posted".format(
            pics[0])
        )
try:
    for pic in pics:
        bot.logger.info("Checking {}".format(pic))
        if args.caption:
            caption = args.caption
        else:
            if captions_for_medias.CAPTIONS.get(pic):
                caption = captions_for_medias.CAPTIONS[pic]
            else:
                try:
                    caption = raw_input(
                        "No caption found for this media. "
                        "Type the caption now: "
                    )
                except NameError:
                    caption = input(
                        "No caption found for this media. "
                        "Type the caption now: "
                    )
        bot.logger.info(
            "Uploading pic `{pic}` with caption: `{caption}`".format(
                pic=pic, caption=caption
            )
        )
        if not bot.upload_photo(
            os.path.dirname(os.path.realpath(__file__)) + "/media/" + pic,
            caption=caption,
        ):
            bot.logger.error("Something went wrong...")
            break
        posted_pic_list.append(pic)
        with open(posted_pic_file, "a") as f:
            f.write(pic + "\n")
        bot.logger.info("Succesfully uploaded: " + pic)
        break
except Exception as e:
    bot.logger.error("\033[41mERROR...\033[0m")
    bot.logger.error(str(e))
