import sys
import os

sys.path.append(os.path.join(sys.path[0], '../../'))
from instabot import Bot

bot = Bot()
bot.login()
assert(bot.like_timeline() == [])
assert(bot.like_user("352300017") == [])
assert(bot.follow_users(["352300017"]) == [])
assert(bot.like_hashtag("mipt") == [])
