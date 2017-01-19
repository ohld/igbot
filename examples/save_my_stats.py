#!/usr/bin/env python
import pandas as pd
import datetime, time
import sys, os

sys.path.append(os.path.join(sys.path[0],'../'))
from instabot import API

def save_stats(api, username):
    """ Saves the number of medias, followers and followed
        into *.tsv file by for future analysis."""

    # get info
    info = api.get_profile_info(username)
    stats = {
        info["date"]: {
                "media": info["media"],
                "follows": info["follows"],
                "followed_by": info["followed_by"]
        }
    }

    # save
    path_to_tsv = "stats_%s.tsv"%(username)
    df = pd.DataFrame.from_dict(stats).T
    if os.path.exists(path_to_tsv):
        df.to_csv(path_to_tsv, mode='a', header=False, sep="\t")
    else:
        df.to_csv(path_to_tsv, header=True, sep="\t")

    return True

if __name__ == "__main__":
    api = API()
    api.login()
    while True:
        save_stats(api, api.user_login)
        print ("Saved at %s"%(datetime.datetime.now()))
        time.sleep(1 * 60 * 60)
    api.logout()
