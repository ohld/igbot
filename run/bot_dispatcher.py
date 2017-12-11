# -*- coding: utf-8 -*-
import argparse
import os
import sys
import codecs
from instabot import Bot
import traceback
from instabot.api import api_db
import math
from datetime import datetime

stdout = sys.stdout
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.path.append(os.path.join(sys.path[0], '../'))


parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-angie_campaign', type=str, help="angie_campaign")
args = parser.parse_args()

if args.angie_campaign is None:
    exit("dispatcher: Campaign id it not specified !")

try:
    bot = Bot(
        id_campaign=args.angie_campaign,
        max_likes_per_day=3100,  # default 1000
        like_delay=20,  # default 10,
        unlike_delay=15,  # default 1-
        multiple_ip=True
    )
  
    campaign = api_db.fetchOne("select username,password,timestamp,id_campaign from campaign where id_campaign=%s", args.angie_campaign)
    bot.canBotStart(args.angie_campaign)
    status = bot.login(username=campaign['username'], password=campaign['password'])
    if status!=True:
        bot.logger.info("dispatcher: Could not login, going to exit !")
        exit()

    calculatedAmount = bot.getAmountDistribution(args.angie_campaign)
    totalExpectedLikesAmount = int(bot.getLikeAmount(args.angie_campaign,calculatedAmount))

    #to do exlude bot
    usersLikeForLike = api_db.fetchOne('select count(*) as total_users from users join user_subscription on (users.id_user = user_subscription.id_user)  join campaign on (users.id_user = campaign.id_user) where (user_subscription.end_date>now() or user_subscription.end_date is null)   and campaign.id_campaign!=%s order by users.id_user',args.angie_campaign)
    bot.logger.info("bot_dispatcher: Total number of likeForLike users: %s", usersLikeForLike['total_users'])
    likeForLikeAmount = usersLikeForLike['total_users']
    
    
    bot.logger.info("bot_dispatcher: Started bot, going to like %s users," % (likeForLikeAmount))

    likeForLikeResult = bot.startLikeForLike(likesAmount=likeForLikeAmount)
    
    bot.logger.info("bot_dispatcher: END. Liked %s users,  expected %s" % (likeForLikeResult, likeForLikeAmount))

except:
  exceptionDetail = traceback.format_exc()
  print(exceptionDetail)
  bot.logger.info("FATAL ERROR !")
  bot.logger.info(exceptionDetail)





