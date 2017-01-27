"""
    instabot example

    Dependencies:
        You must have a "comments_emojie.txt" file which you can find here:
        https://github.com/ohld/instabot/tree/master/examples
        This files contains comments to comment.

    Workflow:
        1) Get your timeline medias
        2) Comment them with random comments from file.

    Notes:
        You can change file and add there your comments.
"""

import time
import sys
import os
from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0],'../'))
from instabot import Bot

comments_file_name = "comments_emojie.txt"
if not os.path.exists(comments_file_name):
    print ("Can't find '%s' file." % comments_file_name)
    exit()

bot = Bot()
bot.login()
for media in tqdm(bot.get_timeline_medias()):
    comment_text = bot.get_comment(comment_base_file=comments_file_name)
    bot.comment(media, comment_text)
    time.sleep(10)
bot.logout()
