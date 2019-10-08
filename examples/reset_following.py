"""

This is a account reset tool.
Use this before you start boting.
You can then reset the users you follow to what you had before botting.

"""
import os
import sys

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot  # noqa: E402


# class of all the tasks
class Task(object):
    # getting the user to pick what to do
    @staticmethod
    def start(bot):
        answer = input(
            """
        Please select
        1) Create Friends List
            Make a list of the users you follow before you follow bot.
        2) Restore Friends List
            Unfollow all user accept for the users in your friends list.
        3) Exit
        \n
        """
        )

        answer = str(answer)
        # make a script
        if answer == "1":
            Task.one(bot)

            # unfollow your nonfriends
        if answer == "2":
            Task.two(bot)

            # exit sript
        if answer == "3":
            exit()

            # invalid input
        else:
            print("Type 1,2 or 3.")
            Task.start(bot)

            # list of followers script

    @staticmethod
    def one(bot):
        print("Creating List")
        friends = bot.following
        with open(
            "friends_{}.txt".format(bot.username), "w"
        ) as file:  # writing to the file
            for user_id in friends:
                file.write(str(user_id) + "\n")
        print("Task Done")
        Task.start(bot)  # go back to the start menu

        # reset following script

    @staticmethod
    def two(bot):
        friends = bot.read_list_from_file(
            "friends_{}.txt".format(bot.username)
        )  # getting the list of friends
        your_following = bot.following
        unfollow = list(
            set(your_following) - set(friends)
        )  # removing your friends from the list to unfollow
        bot.unfollow_users(unfollow)  # unfollowing people who're not friends
        Task.start(bot)  # go back to the start menu


bot = Bot()
bot.login()

# welcome message
print(
    """
    Welcome to this bot.
    It will now get a list of all of the users you are following.
    You will need this if you follow bot your account and you want
    to reset your following to just your friends.
    """
)
Task.start(bot)  # running the start script
