import time
import random
import sys
import os
import getpass
from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], '../../'))
from instabot import Bot

# initial


def initial_checker():
    try:
        fh = open(hashtag_file, 'r')
        fh = open(users_file, 'r')
        fh = open(whitelist, 'r')
        fh = open(blacklist, 'r')
        fh = open(comment, 'r')
        fh = open(setting, 'r')
    except BaseException:
        fh = open(hashtag_file, 'w')
        fh = open(users_file, 'w')
        fh = open(whitelist, 'w')
        fh = open(blacklist, 'w')
        fh = open(comment, 'w')
        fh = open(setting, 'w')
        print("""
        Welcome to instabot, it seems this is the first time you use this bot.
        Before start, let's setting a basic things up first.
        So the bot will function perfectly.
        """)
        setting_input()
        print("""
        You can add hashtag database, competitor database,
        whitelist, and blacklist also add user in setting menu.
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
                "How many like you want to do in a day? (enter to use default number: 999)")
            f.write(str(int(sys.stdin.readline().strip()or "999")) + "\n")
            print("How about unlike? (enter to use default number: 999)")
            f.write(str(int(sys.stdin.readline().strip()or "999")) + "\n")
            print(
                "How many follow you want to do in a day? (enter to use default number: 350)")
            f.write(str(int(sys.stdin.readline().strip()or "350")) + "\n")
            print("How about unfollow? (enter to use default number: 350)")
            f.write(str(int(sys.stdin.readline().strip()or "350")) + "\n")
            print(
                "How many comment you want to do in a day? (enter to use default number:100)")
            f.write(str(int(sys.stdin.readline().strip()or "100")) + "\n")
            print("Maximal likes in media you will like?")
            print(
                "We will skip media that have greater like from this value (enter to use default number: 150)")
            f.write(str(int(sys.stdin.readline().strip()or "150")) + "\n")
            print("Maximal followers of account you want to follow?")
            print("We will skip media that have greater followers from this value (enter to use default number: 2000)")
            f.write(str(int(sys.stdin.readline().strip()or "2000")) + "\n")
            print("Minimal followers of account you want to follow?")
            print(
                "we will skip media that have lesser follower from this value(enter to use default number: 250)")
            f.write(str(int(sys.stdin.readline().strip()or "250")) + "\n")
            print("Maximal following of account you want to follow?")
            print("We will skip media that have greater following from this value (enter to use default number: 5000)")
            f.write(str(int(sys.stdin.readline().strip()or "5000")) + "\n")
            print("Minimal following of account you want to follow?")
            print("we will skip media that have lesser following from this value (enter to use default number: 10)")
            f.write(str(int(sys.stdin.readline().strip()or "10")) + "\n")
            print(
                "Maximal followers to following_ratio (enter to use default number: 10)")
            f.write(str(int(sys.stdin.readline().strip()or "10")) + "\n")
            print("Maximal following to followers_ratio (enter to use default number: 2)")
            f.write(str(int(sys.stdin.readline().strip()or "2")) + "\n")
            print("Minimal media the account you will follow have.")
            print(
                "we will skip media that have lesser media from this value (enter to use default number: 7)")
            f.write(str(int(sys.stdin.readline().strip()or "7")) + "\n")
            print(
                "Delay from one like to another like you will perform (enter to use default number: 30)")
            f.write(str(int(sys.stdin.readline().strip()or "30")) + "\n")
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
            f.write(str(int(sys.stdin.readline().strip()or "None")) + "\n")
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
        print("we will add your instagram account.")
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
    print("current database:")
    print(bot.read_list_from_file(hashtag_file))
    with open(hashtag_file, "a") as f:
        print('Add hashtag to database')
        while True:
            print("Enter hashtag: ")
            f.write(str(sys.stdin.readline().strip()) + "\n")
            print("Do you want to add another hashtag? (y/n)")
            if "y" not in sys.stdin.readline():
                print('done adding hashtag to database')
                break


def competitor_adder():
    print("current database:")
    print(bot.read_list_from_file(users_file))
    with open(users_file, "a") as f:
        print('Add username to database')
        while True:
            print("Enter username: ")
            f.write(str(sys.stdin.readline().strip()) + "\n")
            print("Do you want to add another username? (y/n)")
            if "y" not in sys.stdin.readline():
                print('done adding username to database')
                break


def blacklist_adder():
    print("current database:")
    print(bot.read_list_from_file(blacklist))
    with open(blacklist, "a") as f:
        print('Add username to blacklist')
        while True:
            print("Enter username: ")
            f.write(str(sys.stdin.readline().strip()) + "\n")
            print("Do you want to add another username? (y/n)")
            if "y" not in sys.stdin.readline():
                print('done adding username to blacklist')
                break


def whitelist_adder():
    print("current database:")
    print(bot.read_list_from_file(whitelist))
    with open(whitelist, "a") as f:
        print('Add username to whitelist')
        while True:
            print("Enter username: ")
            f.write(str(sys.stdin.readline().strip()) + "\n")
            print("Do you want to add another username? (y/n)")
            if "y" not in sys.stdin.readline():
                print('done adding username to whitelist')
                break


def comment_adder():
    print("current database:")
    print(bot.read_list_from_file(comment))
    with open(comment, "a") as f:
        print('Add comment')
        while True:
            print("Enter comment: ")
            f.write(str(sys.stdin.readline().strip()) + "\n")
            print("Do you want to add another comment? (y/n)")
            if "y" not in sys.stdin.readline():
                print('done adding comment')
                break


def userlist_maker():
    with open(userlist, "w") as f:
        print('Add user to list')
        while True:
            print("Enter username: ")
            f.write(str(sys.stdin.readline().strip()) + "\n")
            print("Do you want to add another user? (y/n)")
            if "y" not in sys.stdin.readline():
                print('done make list')
                break

# all menu start here


def menu():
    ans = True
    while ans:
        print("""
        1.Follow
        2.like
        3.comment
        4.unfollow
        5.Block
        6.setting
        7.Exit
        """)
        ans = input("What would you like to do?").strip()
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
            bot.logout
            sys.exit()
        else:
            print("\n Not Valid Choice Try again")


def menu_follow():
    ans = True
    while ans:
        print("""
        1. Follow from hashtag
        2. Follow followers
        3. Follow following
        4. Follow someone media likers
        5. Main menu
        """)
        ans = input("how do you want to follow?").strip()

        if ans == "1":
            print("""
            1.insert username
            2.use username database
            """)
            if "1" in sys.stdin.readline():
                user_id = input("who?").strip()
            elif "2" in sys.stdin.readline():
                user_id = random.choice(bot.read_list_from_file(users_file))
            nlikes = input('how much like per account?')
            bot.like_followers(user_id, nlikes=None)

        elif ans == "2":
            print("""
            1.insert username
            2.use username database
            """)
            if "1" in sys.stdin.readline():
                user_id = input("who?").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            bot.follow_followers(user_id)

        elif ans == "3":
            print("""
            1.insert username
            2.use username database
            """)
            if "1" in sys.stdin.readline():
                user_id = input("who?").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            bot.follow_following(user_id)

        elif ans == "4":
            print("""
            1.insert username
            2.use username database
            """)
            if "1" in sys.stdin.readline():
                user_id = input("who?").strip()
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
            print("the number is not in the list you know")
            menu_follow()


def menu_like():
    ans = True
    while ans:
        print("""
        1. Like from hashtag
        2. Like followers
        3. Like following
        4. Like last media likers
        5. Like our timeline
        6. Main menu
        """)
        ans = input("how do you want to like?").strip()

        if ans == "1":
            print("""
            1.insert hashtag
            2.use hashtag database
            """)
            if "1" in sys.stdin.readline():
                hashtag = input("what?").strip()
            else:
                hashtag = random.choice(bot.read_list_from_file(users_file))
            for hashtags in hashtag:
                bot.like_hashtag(hashtags)

        elif ans == "2":
            print("""
            1.insert username
            2.use username database
            """)
            if "1" in sys.stdin.readline():
                user_id = input("who?").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            bot.like_followers(user_id)

        elif ans == "3":
            print("""
            1.insert username
            2.use username database
            """)
            if "1" in sys.stdin.readline():
                user_id = input("who?").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            bot.like_following(user_id)

        elif ans == "4":
            print("""
            1.insert username
            2.use username database
            """)
            if "1" in sys.stdin.readline():
                user_id = input("who?").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            medias = bot.get_user_medias(user_id, filtration=False)
            if len(medias):
                likers = bot.get_media_likers(medias[0])
                for liker in tqdm(likers):
                    bot.like_user(liker, amount=2)

        elif ans == "5":
            bot.like_timeline()

        elif ans == "6":
            menu()

        else:
            print("the number is not in the list you know")
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
        ans = input("how do you want to comment?").strip()

        if ans == "1":
            print("""
            1.insert hashtag
            2.use hashtag database
            """)
            if "1" in sys.stdin.readline():
                hashtag = input("what?").strip()
            else:
                hashtag = random.choice(bot.read_list_from_file(users_file))
            for hashtags in hashtag:
                bot.comment_hashtag(hashtags)

        elif ans == "2":
            print("""
            1.insert username
            2.use username database
            """)
            if "1" in sys.stdin.readline():
                user_id = input("who?").strip()
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
            print("the number is not in the list you know")
            menu_comment()


def menu_unfollow():
    ans = True
    while ans:
        print("""
        1. unfollow non followers
        2. unfollow everyone
        """)
        ans = input("how do you want to unfollow?").strip()

        if ans == "1":
            bot.unfollow_non_followers()

        elif ans == "2":
            bot.unfollow_everyone()

        elif ans == "3":
            menu()

        else:
            print("the number is not in the list you know")
            menu_unfollow()


def menu_block():
    ans = True
    while ans:
        print("""
        1. Block bot
        2. Main menu
        """)
        ans = input("how do you want to block?").strip()
        if ans == "1":
            bot.block_bots()

        elif ans == "2":
            menu()

        else:
            print("the number is not in the list you know")
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
        ans = input("What setting do you need?").strip()

        if ans == "1":
            parameter_setting()
            print("want to change it? y/n").strip()
            if "y" in sys.stdin.readline():
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
                "this will clear all database except your user accounts and paramater settings")
            time.sleep(5)
            fh = open(hashtag_file, 'w')
            fh = open(users_file, 'w')
            fh = open(whitelist, 'w')
            fh = open(blacklist, 'w')
            fh = open(comment, 'w')
            print("done, you can add new one!")
        elif ans == "9":
            menu()
        else:
            print("the number is not in the list you know")
            menu_setting()


# for input compability
if hasattr(__builtins__, 'raw_input'):
    input = raw_input

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
    print("Look like setting are broken")
    print("let's make new one")
    setting_input()

f = open(setting)
lines = f.readlines()
setting_1 = lines[1]
setting_2 = lines[2]
setting_3 = lines[3]
setting_4 = lines[4]
setting_5 = lines[5]
setting_6 = lines[6]
setting_7 = lines[7]
setting_8 = lines[8]
setting_9 = lines[9]
setting_10 = lines[10]
setting_11 = lines[11]
setting_12 = lines[12]
setting_13 = lines[13]
setting_14 = lines[14]
setting_15 = lines[15]
setting_16 = lines[16]
setting_17 = lines[17]
setting_18 = lines[18]

bot = Bot(
    max_likes_per_day=setting_1,
    max_unlikes_per_day=setting_2,
    max_follows_per_day=setting_3,
    max_unfollows_per_day=setting_4,
    max_comments_per_day=setting_5,
    max_likes_to_like=setting_6,
    max_followers_to_follow=setting_7,
    min_followers_to_follow=setting_8,
    max_following_to_follow=setting_9,
    min_following_to_follow=setting_10,
    max_followers_to_following_ratio=setting_11,
    max_following_to_followers_ratio=setting_12,
    min_media_count_to_follow=setting_13,
    like_delay=setting_14,
    unlike_delay=setting_15,
    follow_delay=setting_16,
    unfollow_delay=setting_17,
    comment_delay=setting_18,
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
