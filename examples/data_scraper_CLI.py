"""
This script enables you
To scrape/collect users data and store in a texfile
for use.
"""
from instabot import Bot
import os
import sys
import time

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

bot.logger.info("INSTABOT DATA SCRAPER")
time.sleep(2)

bot.login()
time.sleep(2)
print("What do you want to scrape? (Type number)")
print("%d: %s" % (0, "Someone's Followers"))
print("%d: %s" % (1, "Someones's following"))
print("%d: %s" % (2, "Likers Of Latest Media Of A Page "))
# TODO CONVERT BOTH SCRAPPED FOLLOWERS AND FOLLOWING TO USERNAMES
# TODO GET HASHTAG MEDIAS

scraperMethod = int(sys.stdin.readline())

if scraperMethod == 0:
    print("IF YOU ARE SCRAPING A LARGE AMOUNT OF FOLLOWERS""\nDONT USE THE ACCOUNT YOU BOT WITH TO SCRAPE DATA""\nSCRAPING LARGE DATA CONSUMES TOO MANY REQUESTS""\nWHICH WOULD BE CONSIDERED AS A SPAM")
    time.sleep(3)
    ans = input("Do you want to continue scraping with this account ? yes/no :")
    ans = ans.lower()
    no = bot.login()
    if ans == "no":
        bot.login()

    if ans == "yes":
        SOMEONES_FOLLOWERS = input("what user followers do you want to scrape ? : ")  # get the info of user to be scrapped
        with open('someones_followers_scrape.txt', 'w') as file:
            file.write(SOMEONES_FOLLOWERS)
        pages_to_scrape = bot.read_list_from_file("someones_followers_scrape.txt")  # reading passed "someones followers to  scrape"
        f = open("scrappedFOLLOWERS.txt", "w")  # stored list of "Someone's Followers"
        for follower in pages_to_scrape:
            users = bot.get_user_followers(follower,)
        for userfollowers in users:
            f.write(userfollowers + "\n")
        print("\n" + "successfully written Someone's Followers , to textfile scrappedFOLLOWERS.txt")
        f.close()
        time.sleep(3)
        exit()


elif scraperMethod == 1:
    SOMEONES_FOLLOWING = input("what user following do you want to scrape ? : ")  # get the info of user to be scrapped
    with open('someones_following_scrape.txt', 'w') as file:
        file.write(SOMEONES_FOLLOWING)
    pages_to_scrape1 = bot.read_list_from_file("someones_following_scrape.txt")  # reading passed "someones following to  scrape"
    f1 = open("scrappedFOLLOWINGS.txt", "w")  # stored list of "Someone's Following"
    for followings in pages_to_scrape1:
        users1 = bot.get_user_following(followings)
    for userfollowings in users1:
        f1.write(userfollowings + "\n")
    print("\n" + "successfully written Someone's Followers , to textfile scrappedFOLLOWINGS.txt")
    f1.close()
    time.sleep(3)
    exit()

elif scraperMethod == 2:
    print("THIS FUNCTION ONLY SCRAPES FIRST 1000 LIKERS")
    time.sleep(3)
    LIKERS_OF_A_PAGE = input("what page likers do you want to scrape ? : ")
    with open('likers_of_a_page_scrape.txt', 'w') as file:
        file.write(LIKERS_OF_A_PAGE)
    pages_to_scrape2 = bot.read_list_from_file("likers_of_a_page_scrape.txt")  # reading passed "someones followers to  scrape"
    f2 = open("scrappedLIKERS.txt", "w")  # stored list of "Likers of a page"
    for likers in pages_to_scrape2:
        medias = bot.get_user_medias(likers, filtration=False)
        users2 = bot.get_media_likers(medias[0],)
    for pagelikers in users2:
        f2.write(pagelikers + "\n")
    print("\n" + "successfully written likers of a page , to textfile scrappedLIKERS.txt")
    f2.close()
    time.sleep(3)
    exit()
