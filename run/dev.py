import json

from instabot import Bot
bot = Bot()
bot.login(username="",password="")
result = bot.like_hashtag(hashtag="tuborgromania",amount=3)

#file = open("dump.json","w")
#file.write(json.dumps(result,sort_keys=True, indent=4))
#file.close()
