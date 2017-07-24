"""
    instabot example

    Workflow:
    1) Repost photo to your account
"""

import sys

import os

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot


def repost_photo(my_bot, media_id):
    photo_path = my_bot.download_photo(media_id, description=True)
    if not photo_path:
        return False
    with open(photo_path[:-3] + 'txt', 'r') as f:
        text = ''.join(f.readlines())
    return my_bot.upload_photo(photo_path, text)


media_id = ''

if not media_id:
    print('Media id is empty!')
    exit(1)

bot = Bot()
bot.login()

repost_photo(bot, media_id)
