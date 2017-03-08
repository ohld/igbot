from instabot import Bot

bot = Bot()
bot.login()
bot.like_timeline()
bot.like_user("352300017")
bot.follow_users(["352300017"])
