# coding=utf-8
"""
    instabot example

    Workflow:
        Like medias by location.
"""

import argparse
import os
import sys
import codecs

from tqdm import tqdm

stdout = sys.stdout
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot





id_location=73959962
username="johndoe"
password="password"



bot = Bot()
bot.login(username=username, password=password)

medias = bot.like_posts_by_location(id_location=id_location,amount=5)
