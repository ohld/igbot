from __future__ import unicode_literals

import argparse
import os
import sys

from tqdm import tqdm

# coding=utf-8
"""
    instabot example

    Workflow:
        If media is commented, reply to comments
        if you didn't reply yet to that user.
"""


sys.path.append(os.path.join(sys.path[0], "../../"))
from instabot import Bot  # noqa: E402

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-u", type=str, help="username")
parser.add_argument("-p", type=str, help="password")
parser.add_argument("-proxy", type=str, help="proxy")
parser.add_argument(
    "-comments_file", type=str, help="comments_file", required=True
)
parser.add_argument("-link", type=str, help="media_link", required=True)
args = parser.parse_args()

if not args.comments_file:
    print(
        "You need to pass a path to the file with comments with option\n"
        "-comments_file COMMENTS_FILE_NAME"
    )
    exit()
if not args.link:
    print("You need to pass the media link with option\n" "-link MEDIA_LINK")
    exit()

if not os.path.exists(args.comments_file):
    print("Can't find '{}' file.".format(args.comments_file))
    exit()

bot = Bot(comments_file=args.comments_file)
bot.login(username=args.u, password=args.p, proxy=args.proxy)

media_id = bot.get_media_id_from_link(args.link)
comments = bot.get_media_comments(media_id)
if len(comments) == 0:
    bot.logger.info("Media `{link}` has got no comments yet.".format(
        args.link)
    )
    exit()

commented_users = []
for comment in tqdm(comments):
    replied = False
    parent_comment_id = comment["pk"]
    user_id = comment["user"]["pk"]
    comment_type = comment["type"]
    commenter = comment["user"]["username"]
    text = comment["text"]
    bot.logger.info("Checking comment from `{commenter}`".format(
        commenter=commenter)
    )
    try:
        bot.logger.info("Comment text: `{text}`".format(text=text))
    except Exception as e:
        bot.logger.error("{}".format(e))
    # to save time, because you can't reply to yourself
    if str(user_id) == bot.user_id:
        bot.logger.error("You can't reply to yourself")
        continue
    if user_id in commented_users:
        bot.logger.info("You already replied to this user")
        continue
    for _comment in comments:
        # comments are of type 0 (standard) or type 2 (replies)
        if (
            _comment["type"] == 2
            and str(_comment["user"]["pk"]) == bot.user_id
            and _comment["text"].split(" ")[0][1:] == commenter
        ):
            bot.logger.info("You already replied to this user.")
            replied = True
            break
    if replied:
        continue
    comment_txt = "@{username} {text}".format(
        username=commenter, text=bot.get_comment()
    )
    bot.logger.info(
        "Going to reply to `{username}` with text `{text}`".format(
            username=commenter, text=comment_txt
        )
    )
    if bot.reply_to_comment(media_id, comment_txt, parent_comment_id):
        bot.logger.info("Replied to comment.")
        commented_users.append(user_id)
