"""
instabot example

workflow:
    mention [@user] in comment section
"""
import os
import sys
import argparse
sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-proxy', type=str, help="proxy")
parser.add_argument('user', type=str, help='user')
parser.add_argument('nfollowers', type=int, help='nfollowers')
args = parser.parse_args()

bot = Bot()
bot.login()

userID = bot.get_user_id_from_username(args.user)
someones_followers =  bot.api.get_total_followers_or_followings(userID,
                                                                amount=args.nfollowers,
                                                                filter_private=False,
                                                                filter_business=False,
                                                                filter_verified=False,
                                                                usernames=True,)

medias = bot.get_your_medias()
media_to_comment = medias[0]

for usr in someones_followers:
    comment = '@' + usr['username']
    bot.api.comment(media_to_comment, comment)
    bot.console_print('{} media commented with text: {}'.format(media_to_comment, comment), 'green')
    bot.total['comments'] += 1
    bot.delay('comment')
