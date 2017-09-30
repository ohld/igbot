# -*- coding: utf-8 -*-
import argparse
import codecs
import os
import sys
from instabot.api import api_db

stdout = sys.stdout
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.path.append(os.path.join(sys.path[0], '../'))

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
args = parser.parse_args()

if not args.u or not args.p:
    exit(0)

from instabot import Bot
bot = Bot(id_campaign='1', id_log='1')
bot.login(username=args.u,password=args.p)

#TODO -> maybe create a special function for this (crawl followers or so)
user=api_db.getWebApplicationUser(bot.web_application_id_user)

if not user['followers_next_max_id']:
    next_max_id=None
else:
    next_max_id=user['followers_next_max_id']

result = bot.get_user_followers(user_id=bot.user_id,amount=1000, next_max_id=next_max_id)

if len(result['followers'])==0:
    bot.logger.info("No followers received for user: %s ! SKIPPING", bot.user_id)
    exit(0)

for follower in result['followers']:
    api_db.insertFollower(bot.web_application_id_user,follower['pk'],follower['full_name'],follower['username'],follower['profile_pic_url'],follower['is_verified'])

next_id=result['next_max_id']
if next_id==None:
    next_id=result['previous_next_max_id']

api_db.insert("update users set followers_next_max_id=%s where id_user=%s",next_id,bot.web_application_id_user)

bot.logger.info("DONE updating followers list !")


