# -*- coding: utf-8 -*-
import argparse
import os
import sys
import codecs
from instabot import Bot
import traceback
from instabot.api import api_db
import math
from datetime import datetime

stdout = sys.stdout
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.path.append(os.path.join(sys.path[0], '../'))


parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-username', type=str, help="instagram username")
parser.add_argument('-password', type=str, help="instagram password")
args = parser.parse_args()

if args.username is None:
    exit("dispatcher: Username is not specified !")


try:
    bot = Bot(id_campaign=False,multiple_ip=None)
    status=bot.login(username=args.username, password=args.password)
    print(status)
    print(bot.LastResponse.text)
except:
    exceptionDetail = traceback.format_exc()
    print(exceptionDetail)




