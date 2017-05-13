'''

This is a account reset tool.
Use this before you start boting.
You can then reset the users you follow to what you had before botting.

'''
from instabot import Bot

    #class of all the tasks
class task():

        #geting the user to pick what to do
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

            #make a sript
        if answer=="1":
            task.one()

            #unfollow your nonfriends
        if answer=="2":
            task.two()

            #exit sript
        if answer=="3":
            exit()

            #invald input
        else:
            print("Type 1,2 or 3.")
            task.start()

            #list of followers sript
    def one():
        print("Creating List")
        friends = bot.get_user_following(bot.user_id) #getting following
        friendslist = list(set(friends))    #listing your fiends
        with open("friends.txt", "a") as file:  #writeing to the file
            for user_id in friendslist:
                file.write(str(friendslist) + "\n")
        print("Task Done")
        task.start()    #go back to the start menu

        #reset following sript
    def two():
        friends = bot.read_list_from_file("friends.txt")        #getting the list of friends
        your_following = bot.get_user_following(bot.user_id)    #getting your following
        unfollow = list(set(your_following) - set(friends))     #removing your friends from the list to unfollow
        bot.unfollow_users(unfollow)                            #unfollowing people who are not your friends
        task.start()                                            #go back to the start menu

bot = Bot()
bot.login()

#welcome measage
print ("""
        Welcome to this bot.
        It will now get a list of all of the users you are following.
        You will need this if you follow bot your account and you want to reset your
        following to just your friends.
""")
task.start()    #running the start script
