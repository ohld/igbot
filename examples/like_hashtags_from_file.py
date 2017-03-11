"""
    instabot example

    Workflow:
        Like last images with hashtags from file.
"""

import sys
import os
import time
import random
from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

if len(sys.argv) != 2:
    print("USAGE: Pass a path to the file with hashtags."
           " (one line - one hashtag)")
    print("Example: python %s hashtags.txt" % sys.argv[0])
    exit()

bot = Bot()
hashtags = bot.read_list_from_file(sys.argv[1])
bot.logger.info("Hashtags: " + str(hashtags))
if not hashtags:
    exit()

bot.login()
for hashtag in hashtags:
    bot.like_hashtag(hashtag)
