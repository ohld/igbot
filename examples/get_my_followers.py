#!/usr/bin/env python
import pandas as pd
import datetime
import sys, os

sys.path.append(os.path.join(sys.path[0],'../src'))
from core import Instacore
from prepare import get_credentials

def get_my_followers():
    """Gets followers of logged user. Stores locally in *.csv."""
    login, password = get_credentials()
    core = Instacore(login, password)

    followers = core.get_followers(login)
    df = pd.DataFrame(followers)

    now = datetime.datetime.now()
    df.to_csv("followers_%s_%s.csv"%(login, now.strftime("%Y-%m-%d %H:%M")),
              index=False, encoding="utf8")

    core.logout()
    return True

if __name__ == "__main__":
    get_my_followers()
