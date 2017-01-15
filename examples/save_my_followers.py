#!/usr/bin/env python
import pandas as pd
import datetime
import sys, os

sys.path.append(os.path.join(sys.path[0],'../src'))
from core import Instacore
from prepare import get_credentials

def save_followers(core, username):
    """Gets followers of username. Stores locally in *.csv."""
    followers = core.get_followers(username)
    df = pd.DataFrame(followers)

    now = datetime.datetime.now()
    df.to_csv("followers_%s_%s.csv"%(username, now.strftime("%Y-%m-%d %H:%M")),
              index=False, encoding="utf8")

    core.logout()
    return True

if __name__ == "__main__":
    login, password = get_credentials()
    core = Instacore(login, password)
    save_followers(core, login)
    core.logout()
