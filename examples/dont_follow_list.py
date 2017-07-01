"""

This is a account reset tool.
Use this before you start boting.
You can then reset the users you follow to what you had before botting.

"""
import sys
import os

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot


# class of all the tasks
class Task(object):
    # getting the user to pick what to do
    @staticmethod
    def start(my_bot):
        answer = input("""
        Please select
        1) Create Don't Follow List for Following
            Makes a list of the users you follow before the bot follows.
        2) Create Don't Follow List for Followers
            Makes a list of your following before the bot follows.
        3) Exit
        \n
        """)

        answer = str(answer)
        # make a script
        if answer == '1':
            Task.one(my_bot)

            # unfollow your nonfriends
        if answer == '2':
            Task.two(my_bot)

            # exit sript
        if answer == '3':
            exit()

            # invalid input
        else:
            print("Type 1,2 or 3.")
            Task.start(my_bot)

            # list of followers script

    @staticmethod
    def one(my_bot):
        print("Creating List for Following")
        friends = my_bot.get_user_followers(my_bot.user_id)  # getting following
        friendslist = list(set(friends))  # listing your fiends
        with open("dontFollow.txt", "a") as file:  # writing to the file
            for user_id in friendslist:
                file.write(str(user_id) + "\n")
        print("removing duplicates")
        lines = open('dontFollow.txt', 'r').readlines()
        lines_set = set(lines)
        out  = open('dontFollow.txt', 'w')
        for line in lines_set:
            out.write(line)
        print("Task Done")
        Task.start(my_bot)  # go back to the start menu

        # reset following script

`   @staticmethod
    def two(my_bot):
        print("Creating List for Followers")
        friends = my_bot.get_user_followers(my_bot.user_id)  # getting following
        friendslist = list(set(friends))  # listing your fiends
        with open("dontFollow.txt", "a") as file:  # writing to the file
            for user_id in friendslist:
                file.write(str(user_id) + "\n")
        print("removing duplicates")
        lines = open('dontFollow.txt', 'r').readlines()
        lines_set = set(lines)
        out  = open('dontFollow.txt', 'w')
        for line in lines_set:
            out.write(line)
        print("Task Done")
        Task.start(my_bot)  # go back to the start menu

# reset following script

bot = Bot()
bot.login()

# welcome message
print("""
        Welcome to this bot.
        It will now get a list of all of the users you are following and all your followers.
        You will need this if you don't want your bot to follow someone you don't want to follow. 
""")
Task.start(bot)  # running the start script
