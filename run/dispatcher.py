# -*- coding: utf-8 -*-
import argparse
import os
import sys
import codecs
import json
from instabot import Bot
from instabot.api import api_db
from random import randint

stdout = sys.stdout
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.path.append(os.path.join(sys.path[0], '../'))

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-id_campaign', type=str, help="id_campaign")
parser.add_argument('-operation_type', type=str, help="operationType")
parser.add_argument('-id_log', type=str, help="id_log")
parser.add_argument('-amount', type=int, help='amount')
args = parser.parse_args()


#TODO simplify this file

def getGroupedOperations(configs):
    groupedOperations = {'like': [], 'follow': []}
    for c in configs:
        c = getEnhancedOperation(c)
        if 'like' in c['configName']:
            groupedOperations['like'].append(c)
        # the unfollow operation it's skip at this point. It is executed after follow_users operation.
        # This is a dirty hack maybe it can be improved !
        elif 'follow' in c['configName'] and c['configName'] != "unfollow":
            groupedOperations['follow'].append(c)

    return groupedOperations


def getEnhancedOperation(operation):

    if 'like_other_users_followers' in operation['configName'] or 'follow_other_users_followers' in operation['configName']:

        users = api_db.select("select * from instagram_users where id_config=%s and enabled=1",operation['id_config'])
        operation['list']=users

    if 'like_posts_by_hashtag' in operation['configName'] or 'follow_users_by_hashtag' in operation['configName']:
        hashtags = api_db.select("select * from instagram_hashtags where id_config=%s and enabled=1", operation['id_config'])
        operation['list'] = hashtags

    if 'like_posts_by_location' in operation['configName'] or 'follow_users_by_location' in operation['configName']:
        locations = api_db.select("select * from instagram_locations where id_config=%s and enabled=1", operation['id_config'])
        operation['list'] = locations

    parameters= api_db.select("select * from campaign_config_parameters where id_config=%s", operation['id_config'])

    operation['parameters'] = parameters

    return operation

def handleLikeOperation(bot, availableOperations, opIndex, amount):
    totalAmount = 0

    if 'like_timeline' in availableOperations[opIndex]['configName']:
        bot.logger.info("Bot operation: %s, amount %s", 'like_timeline', amount)
        totalAmount = totalAmount + bot.like_timeline(args.amount)
        del availableOperations[opIndex]
    elif 'like_other_users_followers' in availableOperations[opIndex]['configName']:
        if len(availableOperations[opIndex]['list']) == 0:
            bot.logger.info("No users left for operation like_other_users_followers, skipping this operation...")
            del availableOperations[opIndex]
            return 0
        userIndex = randint(0, len(availableOperations[opIndex]['list']) - 1)
        userObject = availableOperations[opIndex]['list'][userIndex]

        bot.logger.info("Bot operation: %s, instagram user: %s, amount %s", 'like_other_users_followers', userObject['username'] , amount)
       
        totalAmount = totalAmount + bot.like_other_users_followers(userObject, amount=amount)

        del availableOperations[opIndex]['list'][userIndex]

    elif 'like_posts_by_hashtag' in availableOperations[opIndex]['configName']:
        if len(availableOperations[opIndex]['list']) == 0:
            bot.logger.info("No hashtag left for operation like_posts_by_hashtag, skipping this operation...")
            del availableOperations[opIndex]
            return 0

        hashtagIndex = randint(0, len(availableOperations[opIndex]['list']) - 1)
        hashtagObject = availableOperations[opIndex]['list'][hashtagIndex]

        bot.logger.info("Bot operation: %s, hashtag: %s, amount %s", 'like_posts_by_hashtag', hashtagObject['hashtag'], amount)
        totalAmount = totalAmount + bot.like_hashtag(hashtagObject['hashtag'], args.amount)
        # remove the hastagh to no use it again his session
        del availableOperations[opIndex]['list'][hashtagIndex]



    elif 'like_posts_by_location' in availableOperations[opIndex]['configName']:

        if len(availableOperations[opIndex]['list']) == 0:
            bot.logger.info("No location left for operation like_posts_by_location, skipping this operation...")
            del availableOperations[opIndex]
            return 0

        locationIndex = randint(0, len(availableOperations[opIndex]['list']) - 1)
        locationObject = availableOperations[opIndex]['list'][locationIndex]

        bot.logger.info("Bot operation: %s,  location: %s, amount %s", 'like_posts_by_location', locationObject['location'], amount)

        totalAmount = totalAmount + bot.like_posts_by_location(locationObject, args.amount)

        del availableOperations[opIndex]['list'][locationIndex]
    elif 'like_own_followers' in availableOperations[opIndex]['configName']:
        bot.logger.info("Bot operation: %s, amount %s", 'like_own_followers', amount)
        totalAmount = totalAmount + bot.like_own_followers(args.amount)
        del availableOperations[opIndex]
    else:
        bot.logger.info("Invalid operation %s", availableOperations[opIndex]['configName'])

    return totalAmount


def handleFollowOperations(bot, availableOperations, opIndex, amount):
    totalAmount = 0

    if 'follow_users_by_hashtag' in availableOperations[opIndex]['configName']:
        if len(availableOperations[opIndex]['list']) == 0:
            bot.logger.info("No hashtag left for operation follow_users_by_hashtag, skipping this operation...")
            del availableOperations[opIndex]
            return 0

        hashtagIndex = randint(0, len(availableOperations[opIndex]['list']) - 1)
        hashtagObject = availableOperations[opIndex]['list'][hashtagIndex]
        bot.logger.info("Bot operation: %s, hashtag: %s, amount %s", 'follow_users_by_hashtag', hashtagObject['hashtag'], amount)

        totalAmount = totalAmount + bot.follow_users_by_hashtag(hashtag=hashtagObject['hashtag'], amount=args.amount)
        # remove the hastagh to no use it again in this session
        del availableOperations[opIndex]['list'][hashtagIndex]

    elif 'follow_users_by_location' in availableOperations[opIndex]['configName']:
        if len(availableOperations[opIndex]['list']) == 0:
            bot.logger.info("No location left for operation follow_users_by_location, skipping this operation...")
            del availableOperations[opIndex]
            return 0

        locationIndex = randint(0, len(availableOperations[opIndex]['list']) - 1)
        locationObject = availableOperations[opIndex]['list'][locationIndex]

        bot.logger.info("Bot operation: %s, location: %s, amount %s", 'follow_users_by_location', locationObject['location'], amount)

        totalAmount = totalAmount + bot.follow_users_by_location(locationObject, args.amount)

        del availableOperations[opIndex]['list'][locationIndex]
        
    elif 'follow_other_users_followers' in availableOperations[opIndex]['configName']:
        if len(availableOperations[opIndex]['list']) == 0:
            bot.logger.info("No users left for operation follow_other_users_followers, skipping this operation...")
            del availableOperations[opIndex]
            return 0
        userIndex = randint(0, len(availableOperations[opIndex]['list']) - 1)
        userObject = availableOperations[opIndex]['list'][userIndex]

        bot.logger.info("Bot operation: %s, instagram user: %s, amount %s", 'follow_other_users_followers', userObject['username'] , amount)
       
        totalAmount = totalAmount + bot.follow_other_users_followers(userObject, amount=amount)

        del availableOperations[opIndex]['list'][userIndex]
    else:
        bot.logger.info("Invalid operation %s", availableOperations[opIndex]['configName'])

    return totalAmount


bot = Bot(
    id_campaign=args.id_campaign,
    id_log=args.id_log,
    max_likes_per_day=3100,  # default 1000
    max_unlikes_per_day=500,  # default 1000
    max_follows_per_day=230,  # default 350
    max_unfollows_per_day=230,  # default 350
    max_comments_per_day=0,
    max_followers_to_follow=9000000,  # default 2000
    min_followers_to_follow=10,  # default 10
    max_following_to_follow=9000000,  # default 2000
    min_following_to_follow=10,  # default 10
    max_following_to_followers_ratio=4,  # default 2
    min_media_count_to_follow=20,  # default 3
    like_delay=15,  # default 10,
    unlike_delay=15,  # default 1-
    follow_delay=40,  # default 30,
    unfollow_delay=40,  # default 30,
    comment_delay=60,  # default 60
    )

id_campaign = args.id_campaign

campaign = api_db.fetchOne("select username,password from campaign where id_campaign=%s", id_campaign)

bot.login(username=campaign['username'], password=campaign['password'])

configs = api_db.select("SELECT configName,id_config FROM campaign_config where id_campaign=%s and enabled=1", id_campaign)

groupedOperations = getGroupedOperations(configs)

availableOperations = groupedOperations[args.operation_type]

totalAmount = 0
securityBreak = 0

bot.logger.info("Generating random operations of type %s", args.operation_type)

while totalAmount < args.amount and securityBreak < 30:
    if len(availableOperations) == 0:
        bot.logger.info("DONE: No more available operations.")
        break

    opIndex = randint(0, (len(availableOperations) - 1))

    if args.operation_type == "like":
        actionsNumber = handleLikeOperation(bot, availableOperations, opIndex, args.amount)
    elif args.operation_type == "follow":
        actionsNumber = handleFollowOperations(bot, availableOperations, opIndex, args.amount)

    else:
        bot.logger.info("Invalid operation: %s", args.operation_type)

    totalAmount = totalAmount + actionsNumber

    securityBreak = securityBreak + 1



# for each user followed, another one is unfollowed
# todo: maybe this is not a good approach because user might want to unfollow without following
if args.operation_type == "follow":
    totalUsersUnfollowed = bot.unfollowBotCreatedFollowings(amount=args.amount)

bot.crawl_user_followers(amount=1500)

bot.logger.info("DONE dispatcher.py: Total bot actions %s", totalAmount)
