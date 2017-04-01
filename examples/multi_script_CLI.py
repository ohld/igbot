# coding:utf-8
import time
import sys
import os

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

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
        12.Save followers of [username] to TSV
        13.Choose another account of "secret.txt"
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
            # print(bot.stop_words)
        elif ans == "12":
            user = input("Who? ").strip()
            getFollowersToFile(bot, user)
        elif ans == "13":
            bot.login()
        elif ans == "0":
            exit()
        else:
            print("\n Not valid choice. Try again")


def getFollowersToFile(self, user):
    import random, re
    from tqdm import tqdm
    followers = self.getTotalFollowers(self.convert_to_user_id(user))
    out_file_name = 'followers_of_%s.tsv' % user
    out_file = open(out_file_name, 'w')
    out_file.write(
        'full_name\tusername\tpk\tbiography\tfollower_count\tfollowing_count\tis_business\tprofile_pic_url\n')
    i = 0
    for u_name in tqdm(followers, desc='Getting [ %s ] followers' % user):
        try:
            user_info = self.get_user_info(u_name['pk'])
            info = str(str(user_info['full_name']).replace('\n', '').replace(' ', '') + '\t' + user_info['username'] + '\t' + str(user_info['pk']) + '\t' + str(user_info['biography']).replace('\n','') + '\t' + str(user_info['follower_count']) + '\t' + str(user_info['following_count']) + '\t' + str(user_info['is_business']) + '\t' + user_info['profile_pic_url'] + '\n')
            info = re.sub(r'[^\w+|\s|\w|\.|\/]',' ',info)
            out_file.write(info)
            i = i + 1
            # self.logger.info('[%s|%s] %s is added ---> %s' % (str(i), len(followers), u_name['username'], out_file_name))
            time.sleep(random.randrange(1, 10))  # Picked up empirically
        except Exception as e:
            self.logger.warning('User %s not write because: %s' % (user_info['username'], e))

    out_file.close()
    self.logger.info('%s users DONE! You can open the file "%s" using Microsoft Excel' % (str(i), out_file_name))
    time.sleep(5)


bot = Bot(
    max_likes_per_day=1000,
    max_unlikes_per_day=1000,
    max_follows_per_day=1000,
    max_unfollows_per_day=350,
    max_comments_per_day=100,
    max_likes_to_like=50,
    max_followers_to_follow=500,
    min_followers_to_follow=10,
    max_following_to_follow=500,
    min_following_to_follow=10,
    max_followers_to_following_ratio=10,
    max_following_to_followers_ratio=2,
    min_media_count_to_follow=7,
    like_delay=10,
    unlike_delay=10,
    follow_delay=30,
    unfollow_delay=30,
    comment_delay=60,
    # whitelist='whitelist.txt',
    stop_words=['order', 'shop', 'store', 'free', 'doodleartindonesia',
                'doodle art indonesia', 'fullofdoodleart', 'commission',
                'vector', 'karikatur', 'jasa', 'open']
)

bot.logger.info("Multi script run")
print('INSTABOT VERSION: %s ' % bot.version())
# print('Hi, welcome to instabot. I will guide you.')

bot.login()

while True:
    try:
        menu()
    except Exception as e:
        bot.logger.warning(str(e))
    time.sleep(1)
