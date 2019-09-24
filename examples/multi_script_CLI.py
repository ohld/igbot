import getpass
import os
import random
import sys
import time

from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot  # noqa: E402


# initial


def initial_checker():
    files = [hashtag_file, users_file, whitelist, blacklist, comment, setting]
    try:
        for f in files:
            with open(f, "r") as f:
                pass
    except BaseException:
        for f in files:
            with open(f, "w") as f:
                pass
        print(
            """
        Welcome to instabot, it seems this is the first time you've used this bot.
        Before starting, let's setup the basics.
        So the bot functions the way you want.
        """
        )
        setting_input()
        print(
            """
        You can add hashtag database, competitor database,
        whitelists, blacklists and also add users in setting menu.
        Have fun with the bot!
        """
        )
        time.sleep(5)
        os.system("cls")


def read_input(f, msg, n=None):
    if n is not None:
        msg += " (enter to use default number: {})".format(n)
    print(msg)
    entered = sys.stdin.readline().strip() or str(n)
    if isinstance(n, int):
        entered = int(entered)
    f.write(str(entered) + "\n")


# setting function start here
def setting_input():
    inputs = [
        ("How many likes do you want to do in a day?", 1000),
        ("How about unlike? ", 1000),
        ("How many follows do you want to do in a day? ", 350),
        ("How about unfollow? ", 350),
        ("How many comments do you want to do in a day? ", 100),
        (
            (
                "Maximal likes in media you will like?\n"
                "We will skip media that have greater like than this value "
            ),
            100,
        ),
        (
            (
                "Maximal followers of account you want to follow?\n"
                "We will skip media that have greater followers than this value "
            ),
            2000,
        ),
        (
            (
                "Minimum followers a account should have before we follow?\n"
                "We will skip media that have lesser followers than this value "
            ),
            10,
        ),
        (
            (
                "Maximum following of account you want to follow?\n"
                "We will skip media that have a greater following than this value "
            ),
            7500,
        ),
        (
            (
                "Minimum following of account you want to follow?\n"
                "We will skip media that have lesser following from this value "
            ),
            10,
        ),
        ("Maximal followers to following_ratio ", 10),
        ("Maximal following to followers_ratio ", 2),
        (
            (
                "Minimal media the account you will follow have.\n"
                "We will skip media that have lesser media from this value "
            ),
            3,
        ),
        ("Delay from one like to another like you will perform ", 10),
        ("Delay from one unlike to another unlike you will perform ", 10),
        ("Delay from one follow to another follow you will perform ", 30),
        ("Delay from one unfollow to another unfollow you will perform ", 30),
        ("Delay from one comment to another comment you will perform ", 60),
        (
            "Want to use proxy? insert your proxy or leave it blank if no. (just enter",
            "None",
        ),
    ]

    with open(setting, "w") as f:
        while True:
            for msg, n in inputs:
                read_input(f, msg, n)
            break
        print("Done with all settings!")


def parameter_setting():
    settings = [
        "Max likes per day: ",
        "Max unlikes per day: ",
        "Max follows per day: ",
        "Max unfollows per day: ",
        "Max comments per day: ",
        "Max likes to like: ",
        "Max followers to follow: ",
        "Min followers to follow: ",
        "Max following to follow: ",
        "Min following to follow: ",
        "Max followers to following_ratio: ",
        "Max following to followers_ratio: ",
        "Min media_count to follow:",
        "Like delay: ",
        "Unlike delay: ",
        "Follow delay: ",
        "Unfollow delay: ",
        "Comment delay: ",
        "Proxy: ",
    ]

    with open(setting) as f:
        data = f.readlines()

    print("Current parameters\n")
    for s, d in zip(settings, data):
        print(s + d)


def username_adder():
    with open(SECRET_FILE, "a") as f:
        print("We will add your instagram account.")
        print("Don't worry. It will be stored locally.")
        while True:
            print("Enter your login: ")
            f.write(str(sys.stdin.readline().strip()) + ":")
            print("Enter your password: (it will not be shown due to security "
                  "reasons - just start typing and press Enter)")
            f.write(getpass.getpass() + "\n")
            print("Do you want to add another account? (y/n)")
            if "y" not in sys.stdin.readline():
                break


def get_adder(name, fname):
    def _adder():
        print("Current Database:")
        print(bot.read_list_from_file(fname))
        with open(fname, "a") as f:
            print("Add {} to database".format(name))
            while True:
                print("Enter {}: ".format(name))
                f.write(str(sys.stdin.readline().strip()) + "\n")
                print("Do you want to add another {}? (y/n)\n".format(name))
                if "y" not in sys.stdin.readline():
                    print("Done adding {}s to database".format(name))
                    break

    return _adder()


def hashtag_adder():
    return get_adder("hashtag", fname=hashtag_file)


def competitor_adder():
    return get_adder("username", fname=users_file)


def blacklist_adder():
    return get_adder("username", fname=blacklist)


def whitelist_adder():
    return get_adder("username", fname=whitelist)


def comment_adder():
    return get_adder("comment", fname=comment)


def userlist_maker():
    return get_adder("username", userlist)


# all menu start here


def menu():
    ans = True
    while ans:
        print(
            """
        1.Follow
        2.Like
        3.Comment
        4.Unfollow
        5.Block
        6.Setting
        7.Exit
        """
        )
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
        print(
            """
        1. Follow from hashtag
        2. Follow followers
        3. Follow following
        4. Follow by likes on media
        5. Main menu
        """
        )
        ans = input("How do you want to follow?\n").strip()

        if ans == "1":
            print(
                """
            1.Insert hashtag
            2.Use hashtag database
            """
            )
            hashtags = []
            if "1" in sys.stdin.readline():
                hashtags = (
                    input(
                        "Insert hashtags separated by spaces\nExample: cat dog\nwhat hashtags?\n"
                    )
                    .strip()
                    .split(" ")
                )
            else:
                hashtags = bot.read_list_from_file(hashtag_file)
            for hashtag in hashtags:
                print("Begin following: " + hashtag)
                users = bot.get_hashtag_users(hashtag)
                bot.follow_users(users)
            menu_follow()

        elif ans == "2":
            print(
                """
            1.Insert username
            2.Use username database
            """
            )
            if "1" in sys.stdin.readline():
                user_id = input("who?\n").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            bot.follow_followers(user_id)
            menu_follow()

        elif ans == "3":
            print(
                """
            1.Insert username
            2.Use username database
            """
            )
            if "1" in sys.stdin.readline():
                user_id = input("who?\n").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            bot.follow_following(user_id)
            menu_follow()

        elif ans == "4":
            print(
                """
            1.Insert username
            2.Use username database
            """
            )
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
        print(
            """
        1. Like from hashtag(s)
        2. Like followers
        3. Like following
        4. Like last media likers
        5. Like our timeline
        6. Main menu
        """
        )
        ans = input("How do you want to like?\n").strip()

        if ans == "1":
            print(
                """
            1.Insert hashtag(s)
            2.Use hashtag database
            """
            )
            hashtags = []
            if "1" in sys.stdin.readline():
                hashtags = (
                    input(
                        "Insert hashtags separated by spaces\nExample: cat dog\nwhat hashtags?\n"
                    )
                    .strip()
                    .split(" ")
                )
            else:
                hashtags.append(random.choice(bot.read_list_from_file(hashtag_file)))
            for hashtag in hashtags:
                bot.like_hashtag(hashtag)

        elif ans == "2":
            print(
                """
            1.Insert username
            2.Use username database
            """
            )
            if "1" in sys.stdin.readline():
                user_id = input("who?\n").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            bot.like_followers(user_id)

        elif ans == "3":
            print(
                """
            1.Insert username
            2.Use username database
            """
            )
            if "1" in sys.stdin.readline():
                user_id = input("who?\n").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            bot.like_following(user_id)

        elif ans == "4":
            print(
                """
            1.Insert username
            2.Use username database
            """
            )
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
        print(
            """
        1. Comment from hashtag
        2. Comment spesific user media
        3. Comment userlist
        4. Comment our timeline
        5. Main menu
        """
        )
        ans = input("How do you want to comment?\n").strip()

        if ans == "1":
            print(
                """
            1.Insert hashtag
            2.Use hashtag database
            """
            )
            if "1" in sys.stdin.readline():
                hashtag = input("what?").strip()
            else:
                hashtag = random.choice(bot.read_list_from_file(hashtag_file))
            bot.comment_hashtag(hashtag)

        elif ans == "2":
            print(
                """
            1.Insert username
            2.Use username database
            """
            )
            if "1" in sys.stdin.readline():
                user_id = input("who?\n").strip()
            else:
                user_id = random.choice(bot.read_list_from_file(users_file))
            bot.comment_medias(bot.get_user_medias(user_id, filtration=False))

        elif ans == "3":
            print(
                """
            1.Make a list
            2.Use existing list
            """
            )
            if "1" in sys.stdin.readline():
                userlist_maker()
            if "2" in sys.stdin.readline():
                print(userlist)
            users = bot.read_list_from_file(userlist)
            for user_id in users:
                bot.comment_medias(bot.get_user_medias(user_id, filtration=True))

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
        print(
            """
        1. Unfollow non followers
        2. Unfollow everyone
        3. Main menu
        """
        )
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
        print(
            """
        1. Block bot
        2. Main menu
        """
        )
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
        print(
            """
        1. Setting bot parameter
        2. Add user accounts
        3. Add competitor database
        4. Add hashtag database
        5. Add Comment database
        6. Add blacklist
        7. Add whitelist
        8. Clear all database
        9. Main menu
        """
        )
        ans = input("What setting do you need?\n").strip()

        if ans == "1":
            parameter_setting()
            change = input("Want to change it? y/n\n").strip()
            if change == "y" or change == "Y":
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
                "Whis will clear all database except your user accounts and paramater settings"
            )
            time.sleep(5)
            open(hashtag_file, "w")
            open(users_file, "w")
            open(whitelist, "w")
            open(blacklist, "w")
            open(comment, "w")
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
    whitelist_file=whitelist,
    blacklist_file=blacklist,
    comments_file=comment,
    stop_words=[
        "order",
        "shop",
        "store",
        "free",
        "doodleartindonesia",
        "doodle art indonesia",
        "fullofdoodleart",
        "commission",
        "vector",
        "karikatur",
        "jasa",
        "open",
    ],
)

bot.login()

while True:
    try:
        menu()
    except Exception as e:
        bot.logger.info("error, read exception bellow")
        bot.logger.info(str(e))
    time.sleep(1)
