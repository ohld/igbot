'''

This is a account reset tool.

'''
from instabot import Bot

class task():
    def start():
        answer = input("""
        Please select
        1) Create Friends List
            Make a list of the users you follow before you follow bot.
        2) Restore Friends List
            Unfollow all user accept for the users in your friends list.
        3) Exit
        \n
        """)

        if answer=="1":
            task.one()

        if answer=="2":
            task.two()

        if answer=="3":
            exit()
        else:
            print("Type 1,2 or 3.")
            task.start()

    def one():
        print("Creating List")
        friends = bot.get_user_following(bot.user_id)
        friendslist = list(set(friends))
        with open("friends.txt", "a") as file:
            for user_id in friendslist:
                file.write(str(friendslist) + "\n")
        print("Task Done")
        task.start()

    def two():
        friends = bot.read_list_from_file("friends.txt")
        your_following = bot.get_user_following(bot.user_id)
        unfollow = list(set(your_following) - set(friends))
        bot.unfollow_users(unfollow)
        task.start()

bot = Bot()
bot.login()
print ("""
        Welcome to this bot.
        It will now get a list of all of the users you are following.
        You will need this if you follow bot your account and you want to reset your
        following to just your friends.
""")
task.start()
