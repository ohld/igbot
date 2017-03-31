"""
    instabot example

    Dependencies:
        You must have a file with comments to post.
        The file should have one comment per line.

    Notes:
        You can change file and add there your comments.
"""

import time
import sys
import os
from tqdm import tqdm
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

sys.path.append(os.path.join(sys.path[0], '../../'))
from instabot import Bot

if len(sys.argv) < 3:
    print ("USAGE: Pass a path to the file with comments and an hastag to comment")
    print ("Example: %s comments_emojie.txt dog cat" % sys.argv[0])
    exit()

comments_file_name = sys.argv[1]
hashtags = sys.argv[2:]
if not os.path.exists(comments_file_name):
    print ("Can't find '%s' file." % comments_file_name)
    exit()

bot = Bot(comments_file=comments_file_name)
bot.login()
for hashtag in hashtags:
    bot.comment_hashtag(hashtag)
bot.logout()
