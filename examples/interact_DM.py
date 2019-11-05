# -*- coding: utf-8 -*-
"""
    instabot example

    Workflow:
        read and reply your DM
"""

import argparse
import os
import sys

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot  # noqa: E402

try:
    input = raw_input
except NameError:
    pass

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-u", type=str, help="username")
parser.add_argument("-p", type=str, help="password")
parser.add_argument("-proxy", type=str, help="proxy")
args = parser.parse_args()


def choice(message):
    get_choice = input(message)
    if get_choice == "y":
        return True
    elif get_choice == "n":
        return False
    else:
        print("Invalid Input")
        return choice(message)


bot = Bot()
bot.login(username=args.u, password=args.p, proxy=args.proxy)

if bot.api.get_inbox_v2():
    data = bot.last_json["inbox"]["threads"]
    for item in data:
        bot.console_print(item["inviter"]["username"], "lightgreen")
        user_id = str(item["inviter"]["pk"])
        last_item = item["last_permanent_item"]
        item_type = last_item["item_type"]
        if item_type == "text":
            print(last_item["text"])
            if choice("Do you want to reply to this message?(y/n)"):
                text = input("write your message: ")
                if choice("send message?(y/n)"):
                    bot.send_message(
                        text, user_id, thread_id=item["thread_id"]
                    )
                continue
        else:
            print(item_type)
