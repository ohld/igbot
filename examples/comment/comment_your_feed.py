"""
    instabot example

    Dependencies:
        You must have a file with comments to post.
        The file should have one comment per line.

    Workflow:
        1) Get your timeline medias
        2) Comment them with random comments from file.

    Notes:
        You can change file and add there your comments.
"""

import sys
import os

sys.path.append(os.path.join(sys.path[0], "../../"))
from instabot import Bot

if len(sys.argv) != 2:
    print("USAGE: Pass a path to the file with comments")
    print("Example: %s comments_emoji.txt" % sys.argv[0])
    exit()

comments_file_name = sys.argv[1]
if not os.path.exists(comments_file_name):
    print("Can't find '%s' file." % comments_file_name)
    exit()

bot = Bot(comments_file=comments_file_name)
bot.login()
bot.comment_medias(bot.get_timeline_medias())
bot.logout()
