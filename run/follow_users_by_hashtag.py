# -*- coding: utf-8 -*-
import argparse
import os
import sys
import codecs

stdout = sys.stdout
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot


parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-id_campaign', type=str, help="id_campaign")
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-hashtag', type=str,  help='hashtag')
parser.add_argument('-amount', type=int,  help='amount')
args = parser.parse_args()

bot = Bot(id_campaign=args.id_campaign)
bot.login(username=args.u, password=args.p)


feed=bot.getHashtagFeed(args.hashtag,args.amount)
users=[]

for media in feed:
    user = media['user']
    user['media']={}
    user['media']['code'] = media['code']
    user['media']['image'] = media['image_versions2']['candidates'][0]['url']
    user['media']['id']=media['pk']
    users.append(user)

bot.follow_users(users[:args.amount],"follow_users_by_hashtag",args.hashtag)
    
