#!/usr/bin/env python
import pandas as pd
import datetime
import sys, os

sys.path.append(os.path.join(sys.path[0],'../'))
from instabot import API

def save_following(api, username):
    """Gets following of username. Stores locally in *.tsv."""
    following = api.get_following(username)
    df = pd.DataFrame(following)

    now = datetime.datetime.now()
    df.to_csv("following_%s_%s.tsv"%(username, now.strftime("%Y-%m-%d %H:%M")),
              index=False, encoding="utf8", sep="\t")

    return True

if __name__ == "__main__":
    api = API()
    api.login()
    save_following(api, api.user_login)
    api.logout()
