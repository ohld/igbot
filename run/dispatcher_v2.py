# -*- coding: utf-8 -*-
import argparse
import os
import sys
import codecs
from instabot import Bot
import traceback
from instabot.api import api_db
import math



stdout = sys.stdout
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.path.append(os.path.join(sys.path[0], '../'))

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-id_campaign', type=str, help="id_campaign")
parser.add_argument('-id_log', type=str, help="id_log")
args = parser.parse_args()

try:
    bot = Bot(
        id_campaign=args.id_campaign,
        id_log=args.id_log,
        max_likes_per_day=3100,  # default 1000
        max_unlikes_per_day=500,  # default 1000
        max_follows_per_day=800,  # default 350
        max_unfollows_per_day=800,  # default 350
        max_comments_per_day=0,
        max_followers_to_follow=9000000,  # default 2000
        min_followers_to_follow=10,  # default 10
        max_following_to_follow=9000000,  # default 2000
        min_following_to_follow=10,  # default 10
        max_following_to_followers_ratio=4,  # default 2
        min_media_count_to_follow=20,  # default 3
        like_delay=20,  # default 10,
        unlike_delay=15,  # default 1-
        follow_delay=40,  # default 30,
        unfollow_delay=40,  # default 30,
        comment_delay=60,  # default 60
    )

    # assume we trigger this operation 7 times/day
    operationsAmount = bot.getOperationsAmount(args.id_campaign)
    totalExpectedLikesAmount = operationsAmount['likes']
    totalExpectedFollowAmount = operationsAmount['follows']

    numberOfIterations = 2
    currentIteration = 1
    unperformedLikes = 0
    unperformedFollows = 0
    totalPerformedLikes = 0
    totalPerformedFollows = 0
    securityBreak = 20


    campaign = api_db.fetchOne("select username,password from campaign where id_campaign=%s", args.id_campaign)

    bot.login(username=campaign['username'], password=campaign['password'])

    bot.logger.info("DISPATCHER: Started bot, going to perform %s likes, %s follow/unfollow during %s iterations" % (totalExpectedLikesAmount, totalExpectedFollowAmount, numberOfIterations))

    # if we still have some likes or follow to perform
    while (totalPerformedLikes < totalExpectedLikesAmount or totalPerformedFollows < totalExpectedFollowAmount) and currentIteration < securityBreak:
        #if no more likes needed to perform
        if totalExpectedLikesAmount<=totalPerformedLikes:
            currentIterationLikesAmount=0
        else:
            currentIterationLikesAmount = totalExpectedLikesAmount / numberOfIterations

        #if no more follows are needed
        if totalExpectedFollowAmount<=totalPerformedFollows:
            currentIterationFollowAmount = 0
        else:
            currentIterationFollowAmount = totalExpectedFollowAmount / numberOfIterations

        bot.logger.info("DISPATCHER: Started iteration no %s. Going to perform %s likes , %s follow/unfollow" % (
            currentIteration, currentIterationLikesAmount, currentIterationFollowAmount))

        result = bot.start(likesAmount=currentIterationLikesAmount, followAmount=currentIterationFollowAmount,
                           operations=bot.getBotOperations(args.id_campaign))

        totalPerformedLikes = totalPerformedLikes+ result['no_likes']
        totalPerformedFollows= totalPerformedFollows+ result['no_follows']

        bot.logger.info(
            "DISPATCHER: Iteration %s end. Summary: Likes performed %s Likes expected %s . Follows/Unfollow performed %s , Expected follow/unfollow %s .  "
            % (currentIteration, result['no_likes'], currentIterationLikesAmount, result['no_follows'],currentIterationFollowAmount))


        expectedLikesSorFar = ((totalExpectedLikesAmount / numberOfIterations) * currentIteration)
        unperformedLikes = expectedLikesSorFar - totalPerformedLikes if expectedLikesSorFar>=totalPerformedLikes else 0

        expectedFollowSorFar = ((totalExpectedFollowAmount/ numberOfIterations) * currentIteration)
        unperformedFollows = expectedFollowSorFar - totalPerformedFollows if expectedFollowSorFar>= totalPerformedFollows else 0


        bot.logger.info(
            "DISPATCHER: Overall total expected likes so far %s, actual likes %s, unperformed likes: %s , expected follows so far %s, actual follows %s, unperformedFollows: %s" % (expectedLikesSorFar, totalPerformedLikes, unperformedLikes, expectedFollowSorFar, totalPerformedFollows, unperformedFollows))

        bot.logger.info("DISPATCHER:  Total Remained likes to perform %s, total remained follows to perform %s " % (totalExpectedLikesAmount - totalPerformedLikes, totalExpectedFollowAmount - totalPerformedFollows))

        currentIteration = currentIteration + 1

    bot.logger.info(
        "DISPATCHER: BOT END. Summary: Last iteration %s, Likes performed %s Likes expected %s . Follows/Unfollow performed %s , Expected follow/unfollow %s ." % (currentIteration,  totalPerformedLikes, totalExpectedLikesAmount, totalPerformedFollows, totalExpectedFollowAmount))

    #bot.crawl_user_followers(amount=100)
except:
  bot.logger.info("RUNTIME ERROR !")
  exceptionDetail = traceback.format_exc()
  bot.logger.info(exceptionDetail)





