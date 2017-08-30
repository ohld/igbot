# -*- coding: utf-8 -*-
import argparse
import os
import sys
import codecs

stdout = sys.stdout
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot


parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-id_campaign', type=str, help="id_campaign")
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-id_location', type=str,  help='id_location')
parser.add_argument('-amount', type=int,  help='amount')
args = parser.parse_args()


bot = Bot(id_campaign=args.id_campaign)
bot.login(username=args.u, password=args.p)

bot.like_posts_by_location(id_location=args.id_location,amount=args.amount)

