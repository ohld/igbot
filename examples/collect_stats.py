"""
    instabot example

    Collects the information about your account
    every hour in username.tsv file.
"""


from instabot import Bot


bot = Bot()
bot.login(username='m.stikharev', password='123098Maks')

a = bot.get_user_id_from_username("stikharev")
posts = bot.get_last_user_medias(user_id=2088300714, count=3)
print(len(posts))
print(posts)