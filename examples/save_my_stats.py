#!/usr/bin/env python
import pandas as pd
import datetime, time
import sys, os

sys.path.append(os.path.join(sys.path[0],'../src'))
from core import Instacore
from prepare import get_credentials

def save_stats(core, username):
    """ Saves the number of medias, followers and followed
        into *.csv file by for future analysis."""

    # get info
    info = core.get_profile_info(username)
    stats = {
        info["date"]: {
                "media": info["media"],
                "follows": info["follows"],
                "followed_by": info["followed_by"]
        }
    }

    # save
    path_to_csv = "stats_%s.csv"%(username)
    df = pd.DataFrame.from_dict(stats).T
    if os.path.exists(path_to_csv):
        df.to_csv(path_to_csv, mode='a', header=False)
    else:
        df.to_csv(path_to_csv, header=True)

    return True

if __name__ == "__main__":
    login, password = get_credentials()
    core = Instacore(login, password)
    while True:
        save_stats(core, login)
        time.sleep(1 * 60 * 60)
    core.logout()
