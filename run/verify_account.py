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
parser.add_argument('-id_campaign', type=str, help="campaign")
args = parser.parse_args()

if args.u is None:
    exit("dispatcher: Username is not specified !")

result={}
try:
    bot = Bot(id_campaign=args.id_campaign,multiple_ip=True, hide_output=True)
    status=bot.login(username=args.u, password=args.p)
    result["status"]=True
    result["data"]=bot.LastResponse.text
    print(json.dumps(result))
except:
    exceptionDetail = traceback.format_exc()
    result["status"] = False

    if bot.LastResponse != None:
        result["data"] = bot.LastResponse.text
    result["exception"] = exceptionDetail
    print(json.dumps(result))



