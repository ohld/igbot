"""
    instabot example

    Workflow:
        Follow users who post medias with hashtag.
"""

import sys
import os
import time
import random
from tqdm import tqdm
import argparse

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot


bot = Bot()
bot.login(username="catalinbardas",password="atitudinE22")
hashtags=['bucuresti']

for hashtag in hashtags:
    feed=bot.getHashtagFeed(hashtag,2)
    users=[]
    for media in feed:
        user = media['user']
        user['media']={};
        user['media']['code'] = media['code']
        user['media']['image'] = media['image_versions2']['candidates'][0]['url']
        user['media']['post_id']=media['pk']
        users.append(user)
    
if not users[0]['friendship_status']['following']:
    print("user is not following")
else:
    print("user is following")
print(users[0])
