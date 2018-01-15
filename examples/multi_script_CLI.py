import getpass
import os
import random
import sys
import time

from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

# initial


def initial_checker():
    try:
        open(hashtag_file, 'r')
        open(users_file, 'r')
        open(whitelist, 'r')
        open(blacklist, 'r')
        open(comment, 'r')
        open(setting, 'r')
    except BaseException:
        open(hashtag_file, 'w')
        open(users_file, 'w')
        open(whitelist, 'w')
        open(blacklist, 'w')
        open(comment, 'w')
        open(setting, 'w')
        print("""
        Welcome to instabot, it seems this is the first time you've used this bot.
        Before starting, let's setup the basics.
        So the bot functions the way you want.
        """)
        setting_input()
        print("""
        You can add hashtag database, competitor database,
        whitelists, blacklists and also add users in setting menu.
        Have fun with the bot!
        """)
        time.sleep(5)
        os.system('cls')


# language checker
# if 'EN_en' in open(setting).read():
#    print("oke")
#    from lang import EN_en

# setting function start here
def setting_input():
    with open(setting, "w") as f:
        while True:
            print(
                "How many likes do you want to do in a day? (enter to use default number: 1000)")
            f.write(str(int(sys.stdin.readline().strip()or "1000")) + "\n")
            print("How about unlike? (enter to use default number: 1000)")
            f.write(str(int(sys.stdin.readline().strip()or "1000")) + "\n")
            print(
                "How many follows do you want to do in a day? (enter to use default number: 350)")
            f.write(str(int(sys.stdin.readline().strip()or "350")) + "\n")
            print("How about unfollow? (enter to use default number: 350)")
            f.write(str(int(sys.stdin.readline().strip()or "350")) + "\n")
            print(
                "How many comments do you want to do in a day? (enter to use default number:100)")
            f.write(str(int(sys.stdin.readline().strip()or "100")) + "\n")
            print("Maximal likes in media you will like?")
            print(
                "We will skip media that have greater like than this value (enter to use default number: 100)")
            f.write(str(int(sys.stdin.readline().strip()or "100")) + "\n")
            print("Maximal followers of account you want to follow?")
            print("We will skip media that have greater followers than this value (enter to use default number: 2000)")
            f.write(str(int(sys.stdin.readline().strip()or "2000")) + "\n")
            print("Minimum followers a account should have before we follow?")
            print(
                "We will skip media that have lesser followers than this value (enter to use default number: 10)")
            f.write(str(int(sys.stdin.readline().strip()or "10")) + "\n")
            print("Maximum following of account you want to follow?")
            print("We will skip media that have a greater following than this value (enter to use default number: 7500)")
            f.write(str(int(sys.stdin.readline().strip()or "7500")) + "\n")
            print("Minimum following of account you want to follow?")
            print("We will skip media that have lesser following from this value (enter to use default number: 10)")
            f.write(str(int(sys.stdin.readline().strip()or "10")) + "\n")
            print(
                "Maximal followers to following_ratio (enter to use default number: 10)")
            f.write(str(int(sys.stdin.readline().strip()or "10")) + "\n")
            print("Maximal following to followers_ratio (enter to use default number: 2)")
            f.write(str(int(sys.stdin.readline().strip()or "2")) + "\n")
            print("Minimal media the account you will follow have.")
            print(
                "We will skip media that have lesser media from this value (enter to use default number: 3)")
            f.write(str(int(sys.stdin.readline().strip()or "3")) + "\n")
            print(
                "Delay from one like to another like you will perform (enter to use default number: 10)")
            f.write(str(int(sys.stdin.readline().strip()or "10")) + "\n")
            print(
                "Delay from one unlike to another unlike you will perform (enter to use default number: 10)")
            f.write(str(int(sys.stdin.readline().strip()or "10")) + "\n")
            print(
                "Delay from one follow to another follow you will perform (enter to use default number: 30)")
            f.write(str(int(sys.stdin.readline().strip()or "30")) + "\n")
            print(
                "Delay from one unfollow to another unfollow you will perform (enter to use default number: 30)")
            f.write(str(int(sys.stdin.readline().strip()or "30")) + "\n")
            print(
                "Delay from one comment to another comment you will perform (enter to use default number: 60)")
            f.write(str(int(sys.stdin.readline().strip()or "60")) + "\n")
            print(
                "Want to use proxy? insert your proxy or leave it blank if no. (just enter)")
            f.write(str(sys.stdin.readline().strip()) or "None" + "\n")
            print("done with all settings")
            break


def parameter_setting():
    print("current parameter\n")
    f = open(setting)
    data = f.readlines()
    print("Max likes per day: " + data[0])
    print("Max unlikes per day: " + data[1])
    print("Max follows per day: " + data[2])
    print("Max unfollows per day: " + data[3])
    print("Max comments per day: " + data[4])
    print("Max likes to like: " + data[5])
    print("Max followers to follow: " + data[6])
    print("Min followers to follow: " + data[7])
    print("Max following to follow: " + data[8])
    print("Min following to follow: " + data[9])
    print("Max followers to following_ratio: " + data[10])
    print("Max following to followers_ratio: " + data[11])
    print("Min media_count to follow:" + data[12])
    print("Like delay: " + data[13])
    print("Unlike delay: " + data[14])
    print("Follow delay: " + data[15])
    print("Unfollow delay: " + data[16])
    print("Comment delay: " + data[17])
    print("Proxy: " + data[18])


def username_adder():
    with open(SECRET_FILE, "a") as f:
        print("We will add your instagram account.")
        print("Don't worry. It will be stored locally.")
        while True:
            print("Enter your login: ")
            f.write(str(sys.stdin.readline().strip()) + ":")
            print("Enter your password: ")
            f.write(getpass.getpass() + "\n")
            print("Do you want to add another account? (y/n)")
            if "y" not in sys.stdin.readline():
                break


def hashtag_adder():
    print("Current Database:")
    print(bot.read_list_from_file(hashtag_file))
    with open(hashtag_file, "a") as f:
        print('Add hashtag to database')
        while True:
            print("Enter hashtag: ")
            f.write(str(sys.stdin.readline().strip()) + "\n")
            print("Do you want to add another hashtag? (y/n)\n")
            if "y" not in sys.stdin.readline():
                print('Done adding hashtag to database')
                break


def competitor_adder():
    print("Current Database:")
    print(bot.read_list_from_file(users_file))
    with open(users_file, "a") as f:
        print('Add username to database')
        while True:
            print("Enter username: ")
            f.write(str(sys.stdin.readline().strip()) + "\n")
            print("Do you want to add another username? (y/n)\n")
            if "y" not in sys.stdin.readline():
                print('done adding username to database')
                break


def blacklist_adder():
    print("Current Database:")
    print(bot.read_list_from_file(blacklist))
    with open(blacklist, "a") as f:
        print('Add username to blacklist')
        while True:
            print("Enter username: ")
            f.write(str(sys.stdin.readline().strip()) + "\n")
            print("Do you want to add another username? (y/n)\n")
            if "y" not in sys.stdin.readline():
                print('done adding username to blacklist')
                break


def whitelist_adder():
    print("Current Database:")
    print(bot.read_list_from_file(whitelist))
    with open(whitelist, "a") as f:
        print('Add username to whitelist')
        while True:
            print("Enter username: ")
            f.write(str(sys.stdin.readline().strip()) + "\n")
            print("Do you want to add another username? (y/n)\n")
            if "y" not in sys.stdin.readline():
                print('done adding username to whitelist')
                break


def comment_adder():
    print("Current Database:")
    print(bot.read_list_from_file(comment))
    with open(comment, "a") as f:
        print('Add comment')
        while True:
            print("Enter comment: ")
            f.write(str(sys.stdin.readline().strip()) + "\n")
            print("Do you want to add another comment? (y/n)\n")
            if "y" not in sys.stdin.readline():
                print('done adding comment')
                break


def userlist_maker():
    with open(userlist, "w") as f:
        print('Add user to list')
        while True:
            print("Enter username: ")
            f.write(str(sys.stdin.readline().strip()) + "\n")
            print("Do you want to add another user? (y/n)\n")
            if "y" not in sys.stdin.readline():
                print('done make list')
                break

# all menu start here


def menu():
    ans = True
    while ans:
        print("""
        1.Follow
        2.Like
        3.Comment
        4.Unfollow
        5.Block
        6.Setting
        7.Exit
        """)
        ans = input("What would you like to do?\n").strip()
        if ans == "1":
            menu_follow()
        elif ans == "2":
            menu_like()
        elif ans == "3":
            menu_comment()
        elif ans == "4":
            menu_unfollow()
        elif ans == "5":
            menu_block()
        elif ans == "6":
            menu_setting()
        elif ans == "7":
            bot.logout()
            sys.exit()
        else:
            print("\n Not A Valid Choice, Try again")


def menu_follow():
    ans = True
    while ans:
        print("""
        1. Follow from hashtag
        2. Follow followers
        3. Follow following
        4. Follow by likes on media
        5. Main menu
        """)
        ans = input("How do you want to follow?\n").strip()

        if ans == "1":
            print("""
            1.Insert hashtag
            2.Use hashtag database
            """)
            if "1" in sys.stdin.readline():
                hashtag = input("what?\n").strip()
            else:
                hashtag = random.choice(bot.read_list_from_file(hashtag_file))
            users = bot.get_hashtag_users(hashtag)
            bot.follow_users(users)
            menu_follow()

        elif ans == "2":
            print("""
            1.Insert username
            2.Use username database
            """)
            if "1" in sys.stdin.readline():
                user_id = input("who?\n").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            bot.follow_followers(user_id)
            menu_follow()

        elif ans == "3":
            print("""
            1.Insert username
            2.Use username database
            """)
            if "1" in sys.stdin.readline():
                user_id = input("who?\n").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            bot.follow_following(user_id)
            menu_follow()

        elif ans == "4":
            print("""
            1.Insert username
            2.Use username database
            """)
            if "1" in sys.stdin.readline():
                user_id = input("who?\n").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            medias = bot.get_user_medias(user_id, filtration=False)
            if len(medias):
                likers = bot.get_media_likers(medias[0])
                for liker in tqdm(likers):
                    bot.follow(liker)

        elif ans == "5":
            menu()

        else:
            print("This number is not in the list?")
            menu_follow()


def menu_like():
    ans = True
    while ans:
        print("""
        1. Like from hashtag(s)
        2. Like followers
        3. Like following
        4. Like last media likers
        5. Like our timeline
        6. Main menu
        """)
        ans = input("How do you want to like?\n").strip()

        if ans == "1":
            print("""
            1.Insert hashtag(s)
            2.Use hashtag database
            """)
            hashtags = []
            if "1" in sys.stdin.readline():
                hashtags = input("Insert hashtags separated by spaces\nExample: cat dog\nwhat hashtags?\n").strip().split(' ')
            else:
                hashtags.append(random.choice(bot.read_list_from_file(hashtag_file)))
            for hashtag in hashtags:
                bot.like_hashtag(hashtag)

        elif ans == "2":
            print("""
            1.Insert username
            2.Use username database
            """)
            if "1" in sys.stdin.readline():
                user_id = input("who?\n").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            bot.like_followers(user_id)

        elif ans == "3":
            print("""
            1.Insert username
            2.Use username database
            """)
            if "1" in sys.stdin.readline():
                user_id = input("who?\n").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            bot.like_following(user_id)

        elif ans == "4":
            print("""
            1.Insert username
            2.Use username database
            """)
            if "1" in sys.stdin.readline():
                user_id = input("who?\n").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            medias = bot.get_user_medias(user_id, filtration=False)
            if len(medias):
                likers = bot.get_media_likers(medias[0])
                for liker in tqdm(likers):
                    bot.like_user(liker, amount=2, filtration=False)

        elif ans == "5":
            bot.like_timeline()

        elif ans == "6":
            menu()

        else:
            print("This number is not in the list?")
            menu_like()


def menu_comment():
    ans = True
    while ans:
        print("""
        1. Comment from hashtag
        2. Comment spesific user media
        3. Comment userlist
        4. Comment our timeline
        5. Main menu
        """)
        ans = input("How do you want to comment?\n").strip()

        if ans == "1":
            print("""
            1.Insert hashtag
            2.Use hashtag database
            """)
            if "1" in sys.stdin.readline():
                hashtag = input("what?").strip()
            else:
                hashtag = random.choice(bot.read_list_from_file(hashtag_file))
            bot.comment_hashtag(hashtag)

        elif ans == "2":
            print("""
            1.Insert username
            2.Use username database
            """)
            if "1" in sys.stdin.readline():
                user_id = input("who?\n").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            bot.comment_medias(bot.get_user_medias(user_id, filtration=False))

        elif ans == "3":
            print("""
            1.Make a list
            2.Use existing list
            """)
            if "1" in sys.stdin.readline():
                userlist_maker()
            if "2" in sys.stdin.readline():
                print(userlist)
            users = bot.read_list_from_file(userlist)
            for user_id in users:
                bot.comment_medias(
                    bot.get_user_medias(
                        user_id, filtration=True))

        elif ans == "4":
            bot.comment_medias(bot.get_timeline_medias())

        elif ans == "5":
            menu()

        else:
            print("This number is not in the list?")
            menu_comment()


def menu_unfollow():
    ans = True
    while ans:
        print("""
        1. Unfollow non followers
        2. Unfollow everyone
        """)
        ans = input("How do you want to unfollow?\n").strip()

        if ans == "1":
            bot.unfollow_non_followers()
            menu_unfollow()

        elif ans == "2":
            bot.unfollow_everyone()
            menu_unfollow()

        elif ans == "3":
            menu()

        else:
            print("This number is not in the list?")
            menu_unfollow()


def menu_block():
    ans = True
    while ans:
        print("""
        1. Block bot
        2. Main menu
        """)
        ans = input("how do you want to block?\n").strip()
        if ans == "1":
            bot.block_bots()
            menu_block()

        elif ans == "2":
            menu()

        else:
            print("This number is not in the list?")
            menu_block()


def menu_setting():
    ans = True
    while ans:
        print("""
        1. Setting bot parameter
        2. Add user accounts
        3. Add competitor database
        4. Add hashtag database
        5. Add Comment database
        6. Add blacklist
        7. Add whitelist
        8. Clear all database
        9. Main menu
        """)
        ans = input("What setting do you need?\n").strip()

        if ans == "1":
            parameter_setting()
            change = input("Want to change it? y/n\n").strip()
            if change == 'y' or change == 'Y':
                setting_input()
            else:
                menu_setting()
        elif ans == "2":
            username_adder()
        elif ans == "3":
            competitor_adder()
        elif ans == "4":
            hashtag_adder()
        elif ans == "5":
            comment_adder()
        elif ans == "6":
            blacklist_adder()
        elif ans == "7":
            whitelist_adder()
        elif ans == "8":
            print(
                "Whis will clear all database except your user accounts and paramater settings")
            time.sleep(5)
            open(hashtag_file, 'w')
            open(users_file, 'w')
            open(whitelist, 'w')
            open(blacklist, 'w')
            open(comment, 'w')
            print("Done, you can add new one!")
        elif ans == "9":
            menu()
        else:
            print("This number is not in the list?")
            menu_setting()


# for input compability
try:
    input = raw_input
except NameError:
    pass

# files location
hashtag_file = "hashtagsdb.txt"
users_file = "usersdb.txt"
whitelist = "whitelist.txt"
blacklist = "blacklist.txt"
userlist = "userlist.txt"
comment = "comment.txt"
setting = "setting.txt"
SECRET_FILE = "secret.txt"

# check setting first
initial_checker()

if os.stat(setting).st_size == 0:
    print("Looks like setting are broken")
    print("Let's make new one")
    setting_input()

f = open(setting)
lines = f.readlines()
setting_0 = int(lines[0].strip())
setting_1 = int(lines[1].strip())
setting_2 = int(lines[2].strip())
setting_3 = int(lines[3].strip())
setting_4 = int(lines[4].strip())
setting_5 = int(lines[5].strip())
setting_6 = int(lines[6].strip())
setting_7 = int(lines[7].strip())
setting_8 = int(lines[8].strip())
setting_9 = int(lines[9].strip())
setting_10 = int(lines[10].strip())
setting_11 = int(lines[11].strip())
setting_12 = int(lines[12].strip())
setting_13 = int(lines[13].strip())
setting_14 = int(lines[14].strip())
setting_15 = int(lines[15].strip())
setting_16 = int(lines[16].strip())
setting_17 = int(lines[17].strip())
setting_18 = lines[18].strip()

bot = Bot(
    max_likes_per_day=setting_0,
    max_unlikes_per_day=setting_1,
    max_follows_per_day=setting_2,
    max_unfollows_per_day=setting_3,
    max_comments_per_day=setting_4,
    max_likes_to_like=setting_5,
    max_followers_to_follow=setting_6,
    min_followers_to_follow=setting_7,
    max_following_to_follow=setting_8,
    min_following_to_follow=setting_9,
    max_followers_to_following_ratio=setting_10,
    max_following_to_followers_ratio=setting_11,
    min_media_count_to_follow=setting_12,
    like_delay=setting_13,
    unlike_delay=setting_14,
    follow_delay=setting_15,
    unfollow_delay=setting_16,
    comment_delay=setting_17,
    whitelist=whitelist,
    blacklist=blacklist,
    comments_file=comment,
    stop_words=[
        'order',
        'shop',
        'store',
        'free',
        'doodleartindonesia',
        'doodle art indonesia',
        'fullofdoodleart',
        'commission',
        'vector',
        'karikatur',
        'jasa',
        'open'])

bot.login()

while True:
    try:
        menu()
    except Exception as e:
        bot.logger.info("error, read exception bellow")
        bot.logger.info(str(e))
    time.sleep(1)
