import time
import sys
import os
from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], '../'))
from examples import config_bot
bot = config_bot.bot


if hasattr(__builtins__, 'raw_input'):
    input = raw_input


def menu():
    ans = True
    while ans:
        print("""
        1.Like hashtags
        2.Like followers of
        3.Like following of
        4.Like your timeline feed
        5.Follow users by hashtags
        6.Follow followers of
        7.Follow following of
        8.Unfollow non followers
        9.Unfollow everyone
        10.Block bots
        11.Load stop words from file 'stop_words.txt'
        0.Exit
        """)
        ans = input("What would you like to do? ").strip()
        if ans == "1":
            hashtags = input("What hashtags? ").split()
            amount = input("How much likes? ")
            for hashtag in hashtags:
                bot.like_hashtag(hashtag, amount=int(amount))
        elif ans == "2":
            user_id = input("Who? ").strip()
            nlikes = input("How much like per account? ")
            bot.like_followers(user_id, nlikes=int(nlikes))
        elif ans == "3":
            user_id = input("Who? ").strip()
            nlikes = input("How much like per account? ")
            bot.like_following(user_id, nlikes=int(nlikes))
        elif ans == "4":
            bot.like_timeline()
        elif ans == "5":
            hashtags = input("What hashtags? ").split()
            for hashtag in hashtags:
                bot.follow_users(bot.get_hashtag_users(hashtag))
        elif ans == "6":
            user_id = input("Who? ").strip()
            bot.follow_followers(user_id)
        elif ans == "7":
            user_id = input("Who? ").strip()
            bot.follow_following(user_id)
        elif ans == "8":
            bot.unfollow_non_followers()
        elif ans == "9":
            bot.unfollow_everyone()
        elif ans == "10":
            bot.block_bots()
        elif ans == "11":
            new_words = bot.read_list_from_file('stop_words.txt')
            bot.stop_words.extend(new_words)
        elif ans == "0":
            exit()
        else:
            print("\n Not valid choice. Try again")

bot.logger.info("Multi script run")
print('Hi, welcome to instabot. I will guide you.')
bot.login()

while True:
    try:
        menu()
    except Exception as e:
        bot.logger.warning(str(e))
    time.sleep(1)
