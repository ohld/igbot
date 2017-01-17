#!/usr/bin/env python
import pandas as pd
import datetime
import sys, os

sys.path.append(os.path.join(sys.path[0],'../'))
from instabot import API

def save_followers(api, username):
    """Gets followers of username. Stores locally in *.csv."""
    followers = api.get_followers(username)
    df = pd.DataFrame(followers)

    now = datetime.datetime.now()
    df.to_csv("followers_%s_%s.csv"%(username, now.strftime("%Y-%m-%d %H:%M")),
              index=False, encoding="utf8")

    api.logout()
    return True

if __name__ == "__main__":
    api = API()
    save_followers(api, api.user_login)
    api.logout()
