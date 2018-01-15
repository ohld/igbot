"""

This is a account reset tool.
Use this before you start boting.
You can then reset the users you follow to what you had before botting.

"""
import os
import sys

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot


# class of all the tasks
class Task(object):
    # getting the user to pick what to do
    @staticmethod
    def start(my_bot):
        answer = input("""
        Please select
        1) Create Friends List
            Make a list of the users you follow before you follow bot.
        2) Restore Friends List
            Unfollow all user accept for the users in your friends list.
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
        print("Creating List")
        friends = my_bot.get_user_following(my_bot.user_id)  # getting following
        friendslist = list(set(friends))  # listing your fiends
        with open("friends_{0}.txt".format(my_bot.username), "w") as file:  # writing to the file
            for user_id in friendslist:
                file.write(str(user_id) + "\n")
        print("Task Done")
        Task.start(my_bot)  # go back to the start menu

        # reset following script

    @staticmethod
    def two(my_bot):
        friends = my_bot.read_list_from_file("friends_{0}.txt".format(my_bot.username))  # getting the list of friends
        your_following = bot.get_user_following(my_bot.user_id)  # getting your following
        unfollow = list(set(your_following) - set(friends))  # removing your friends from the list to unfollow
        bot.unfollow_users(unfollow)  # unfollowing people who are not your friends
        Task.start(my_bot)  # go back to the start menu


bot = Bot()
bot.login()

# welcome message
print("""
        Welcome to this bot.
        It will now get a list of all of the users you are following.
        You will need this if you follow bot your account and you want to reset your
        following to just your friends.
""")
Task.start(bot)  # running the start script
