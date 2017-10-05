"""
    instabot example

    Workflow:
    1) Ask Message type
    2) Load messages CSV (if needed)
    3) Send message to each users

"""

import sys
import os
import csv
import time

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

instaUsers = ["R1B4Z01D","KoanMedia"];
directMessage = ["Thanks for the example."];

messagesToSend = 100
banDelay = (86400/messagesToSend)

print("Which type of delivery method? (Type number)")
print("%d: %s" % (0, "Messages From CSV File."))
print("%d: %s" % (1, "Group Message All Users From List."))
print("%d: %s" % (2, "Message Each User From List."))

deliveryMethod = int(sys.stdin.readline())

bot = Bot()
bot.login()

if deliveryMethod == 0:
    with open('messages.csv', 'rU') as f:
        reader = csv.reader(f)
        for row in reader:
            print('Messaging ' + row[0])
            bot.send_message(row[1], row[0])
            print('Waiting ' + str(banDelay) + ' seconds...')
            time.sleep(banDelay)
elif deliveryMethod == 1:
    bot.send_message(directMessage, instaUsers)
    print('Sent A Group Message To All Users..')
elif deliveryMethod == 2:
    bot.send_messages(directMessage, instaUsers)
    print('Sent An Individual Messages To All Users..')
else:
    print('Invalid Selection.')