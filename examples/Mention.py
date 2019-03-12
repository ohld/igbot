"""
instabot example

workflow:
    mention [@user] in comment section
"""
import os
import sys
import random
from termcolor import colored
from instabot import Bot
sys.path.append(os.path.join(sys.path[0], '../'))


bot = Bot(comments_file="mentionlist.txt",
			comment_delay=3,)
bot.login()


# get a list of users to mention and store in a text file


someones_followers = input(colored("what user followers do you want to scrape ? : ", 'red'))  # scrape users followers
with open('someones_followers_scrape.txt', 'w') as file:
    file.write(someones_followers)
pages_to_scrape = bot.read_list_from_file("someones_followers_scrape.txt")  # reading passed "someones followers to  scrape"
f = open("scrappedFOLLOWERS.txt", "w")  # stored list of "Someone's Followers"
for follower in pages_to_scrape:
    users = bot.get_user_followers(follower,30)
for userfollowers in users:
    f.write(userfollowers + "\n")
print(colored("\n" + "successfully written Someone's Followers , to textfile scrappedFOLLOWERS.txt", 'green'))
f.close()

# convert passed scrapped followers to usernames


print(colored("Converting scrappedFOLLOWERS.txt to usernames, MIGHT TAKE AWHILE!!!!", 'red'))
wusers = bot.read_list_from_file("scrappedFOLLOWERS.txt")
with open("usernamelist.txt", 'w+') as f:
	for list in wusers:
		usernames=bot.get_username_from_user_id(list) + '\n'
		f.write(usernames)
	print(colored("succesfully converted  " + str(wusers), 'green'))

# append '@' to scrapped list


print("adding '@' to usernames")
appendText = '@'
followlist = open("usernamelist.txt", 'r')
updatedList = open("mentionlist.txt", 'w')
for name in followlist:
    updatedList.write(appendText + name.rstrip() + '\n')
updatedList.close()
print(colored("succesfully appended '@' to usernames", 'green'))


# comment @users on last media post
medias=bot.get_your_medias()
while True:
	bot.comment_medias([medias[0]])
