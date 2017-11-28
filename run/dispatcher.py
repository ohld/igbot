# -*- coding: utf-8 -*-
import argparse
import os
import sys
import codecs
import json
from instabot import Bot
from instabot.api import api_db
from random import randint
import traceback
import time
from datetime import datetime


totalPerformedLikes=0
totalPerformedFollows=0
totalExpectedLikesAmount =20
totalExpectedFollowAmount=5
currentIteration = 0
securityBreak=6

startingDate=datetime.now().date()





while (totalPerformedLikes < totalExpectedLikesAmount or totalPerformedFollows < totalExpectedFollowAmount) and currentIteration < securityBreak and startingDate.day==datetime.now().date().day:
  print("startingDate="+str(startingDate.day))
  print("currentDate=" +str(datetime.now().date().day))
  totalPerformedLikes=totalPerformedLikes+1
  totalPerformedFollows = totalPerformedFollows + 1
  securityBreak = securityBreak +1
  time.sleep(1)
  
