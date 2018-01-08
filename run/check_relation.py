# -*- coding: utf-8 -*-
import argparse
import codecs
import os
import sys
import traceback
import json
from instabot import Bot

stdout = sys.stdout
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.path.append(os.path.join(sys.path[0], '../'))


parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="instagram username")
parser.add_argument('-p', type=str, help="instagram password")
args = parser.parse_args()

if args.u is None:
    exit("dispatcher: Username is not specified !")


try:
    bot = Bot(id_campaign=False,multiple_ip=False)
    bot.login(username=args.u, password=args.p)
    username = bot.get_user_info('53463941')



except:
    exceptionDetail = traceback.format_exc()
    print(exceptionDetail)




