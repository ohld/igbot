import time
import sys
import os
from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], '../../'))
from instabot import Bot

if hasattr(__builtins__, 'raw_input'):
    input = raw_input

bot = Bot(
    max_likes_per_day=1000,
    max_unlikes_per_day=1000,
    max_follows_per_day=350,
    max_unfollows_per_day=350,
    max_comments_per_day=100,
    max_likes_to_like=100,
    max_followers_to_follow=2000,
    min_followers_to_follow=250,
    max_following_to_follow=10000,
    min_following_to_follow=10,
    max_followers_to_following_ratio=10,
    max_following_to_followers_ratio=2,
    min_media_count_to_follow=7,
    like_delay=10,
    unlike_delay=10,
    follow_delay=30,
    unfollow_delay=30,
    comment_delay=60,
    stop_words=['order', 'shop', 'store', 'free', 'doodleartindonesia', 'doodle art indonesia',
                'fullofdoodleart', 'commission', 'vector', 'karikatur', 'jasa', 'open']
)
bot.logger.info("Multi script run")
print('Hi, welcome to instabot. I will guide you.')

#username=input("Your username?")
#password=getpass.getpass("Your password? (Don't worry. Store in local)")
bot.login()


def menu():
    ans = True
    while ans:
        print("""
        1.Like hashtags
        2.Like followers of
        3.Like following of
        4.Like our feeds
        5.Follow from hashtags
        6.Follow followers of
        7.Follow following of
        8.Unfollow non followers
        9.Unfollow everyone
        """)
        ans = input("What would you like to do?").strip()
        if ans == "1":
            hashtag = input("what hashtag?")
            amount = input("how much like?")
            bot.like_hashtag(hashtag, amount=None)
        elif ans == "2":
            user_id = input("who?")
            nlikes = input('how much like per account?')
            bot.like_followers(user_id, nlikes=None)
        elif ans == "3":
            user_id = input("who?")
            nlikes = input('how much like per account?')
            bot.like_following(user_id, nlikes=None)
        elif ans == "4":
            bot.like_timeline()
        elif ans == "5":
            hashtag = input("what hashtag?")
            bot.follow_users(bot.get_hashtag_users(hashtag))
        elif ans == "6":
            user_id = input("who?")
            bot.follow_followers(user_id)
        elif ans == "7":
            user_id = input("who?")
            bot.follow_following(user_id)
        elif ans == "8":
            bot.unfollow_non_followers()
        elif ans == "9":
            bot.unfollow_everyone()
# try to implement update database for hashtags or users but no luck.
#        elif ans=="11":
#            thelist = []
#            maxLengthList = 5
#            while len(thelist) < maxLengthList:
#                item = input("Enter your hashtag to database: ")
#                thelist.append(item)
#                print thelist
#                print "add another"
#                with open('hashtags.txt', 'w') as file_handler:
#                        file_handler.write("{}\n".format(thelist)
        else:
            print("\n Not Valid Choice Try again")


while True:
    try:
        menu()
    except Exception as e:
        bot.logger.info("error, read exception bellow")
        bot.logger.info(str(e))
    time.sleep(1)
