import time
import sys
import os
from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

if hasattr(__builtins__, 'raw_input'):
    input = raw_input


def menu():
    ans = True
    while ans:
        print("""
        1.Like hashtags
        2.Like followers of [username]
        3.Like following of [username]
        4.Like your timeline feed
        5.Follow users by hashtags
        6.Follow followers of [username]
        7.Follow following of [username]
        8.Unfollow non followers
        9.Unfollow everyone
        10.Block bots
        11.Load stop words from file 'stop_words.txt'
        12.Save followers of [username] to XLSX
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
        elif ans == "12":
            user = input("Who? ").strip()
            getFollowersToFile(user)
        elif ans == "13":
            bot.login()
        elif ans == "0":
            exit()
        else:
            print("\n Not valid choice. Try again")
            
def getFollowersToFile(user):
    import xlsxwriter, random
    
    followers = bot.getTotalFollowers(bot.convert_to_user_id(user))
    workbook = xlsxwriter.Workbook('followers_of_%s.xlsx' % user)
    worksheet = workbook.add_worksheet()
    worksheet.set_column('A:A', 20)
    bold = workbook.add_format({'bold': True})
    worksheet.write('A1', 'full_name'.upper(), bold)
    worksheet.write('B1', 'username'.upper(), bold)
    worksheet.write('C1', 'pk'.upper(), bold)
    worksheet.write('D1', 'biography'.upper(), bold)
    worksheet.write('E1', 'follower_count'.upper(), bold)
    worksheet.write('F1', 'following_count'.upper(), bold)
    worksheet.write('G1', 'is_business'.upper(), bold)
    worksheet.write('H1', 'profile_pic_url'.upper(), bold)
    i = 1

    for u_name in followers:
        user_info = bot.get_user_info(u_name['pk'])
        bot.logger.info('[%s|%s] %s is added ---> %s.xlsx' % (str(i), len(followers), u_name['username'], user))
        i = i + 1
        worksheet.write('A'+str(i),user_info['full_name'])
        worksheet.write('B'+str(i),user_info['username'])
        worksheet.write('C'+str(i),user_info['pk'])
        worksheet.write('D'+str(i),user_info['biography'])
        worksheet.write('E'+str(i),user_info['follower_count'])
        worksheet.write('F'+str(i),user_info['following_count'])
        worksheet.write('G'+str(i),user_info['is_business'])
        worksheet.write_url('H' + str(i), user_info['profile_pic_url'])

        time.sleep(random.randrange(1,10))
    workbook.close()
    bot.logger.info('Done!')

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
    stop_words=['order', 'shop', 'store', 'free', 'doodleartindonesia',
                'doodle art indonesia', 'fullofdoodleart', 'commission',
                'vector', 'karikatur', 'jasa', 'open']
)
bot.logger.info("Multi script run")
print('Hi, welcome to instabot. I will guide you.')
bot.login()

while True:
    try:
        menu()
    except Exception as e:
        bot.logger.warning(str(e))
    time.sleep(1)
