import MySQLdb
import sys
import json

import sys
import os

sys.path.append(os.path.join(sys.path[0], '../'))

from instabot import Bot
bot = Bot(
    max_likes_per_day=350,  # default 1000
    max_unlikes_per_day=500,  # default 1000
    max_follows_per_day=100,  # default 350
    max_unfollows_per_day=100,  # default 350
    max_comments_per_day=0,
    max_likes_to_like=10000,  # default 100
    max_followers_to_follow=30000,  # default 2000
    min_followers_to_follow=100,  # default 10
    max_following_to_follow=30000,  # default 2000
    min_following_to_follow=100,  # default 10
    max_followers_to_following_ratio=15,  # default 10
    max_following_to_followers_ratio=3,  # default 2
    min_media_count_to_follow=10,  # default 3
    like_delay=15,  # default 10,
    unlike_delay=15,  # default 1-
    follow_delay=40,  # default 30,
    unfollow_delay=40,  # default 30,
    comment_delay=60,  # default 60,
    stop_words=[
        'order',
        'shop',
        'store',
        'free',
        'fullofdoodleart',
        'commission',
        'vector',
        'karikatur',
        'jasa',
        'open'])

id_campaign = sys.argv[1]
db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                     user="root",  # your username
                     passwd="password",  # your password
                     db="instaboost")
cur = db.cursor(MySQLdb.cursors.DictCursor)

cur.execute("select username,password from campaign where id_campaign=" + id_campaign)
campaign = cur.fetchone()

bot.login(username=campaign['username'], password=campaign['password'])

cur.execute("SELECT configName,parameters FROM campaign_config where id_campaign=" + id_campaign)
rows = cur.fetchall()
db.close()

# print all the first cell of all the rows
for row in rows:

    # like timeline
    if row['configName'] == "like_timeline":
        config = json.loads(row['parameters'])
        print("Going to like " + str(config['amount']) + " the timeline")
        # like timeline
        bot.like_timeline(config['amount'])

    # like hashtag
    elif row['configName'] == "like_hashtag":
        config = json.loads(row['parameters'])
        print("Going to like " + str(config['amount']) + " posts foreach hashtag:")
        for hashtag in config['list']:
            print(hashtag)
            bot.like_hashtag(hashtag, config['amount'])

    # like followers
    elif row['configName'] == "like_followers":
        config = json.loads(row['parameters'])
        print("Going to like " + str(config['amount']) + " posts of followers of  each user:")

        for username in config['list']:
            bot.like_followers(username, config['amount'])
            print(username)

    # follow followers
    elif row['configName'] == "follow_followers":
        config = json.loads(row['parameters'])
        print("Going to follow " + str(config['amount']) + " followers of each users:")

        for username in config['list']:
            bot.follow_followers(username,config['amount'])
            print(username)
    else:
        print("Unknown command:" + row['configName'])
