import time
import random
import json

def unfollow_non_followers(bot):
    print ("Unfollow non followers:")
    followings = set([item["pk"] for item in bot.getTotalSelfFollowings()])
    print ("  You follow %d users." % len(followings))
    followers = set([item["pk"] for item in bot.getTotalSelfFollowers()])
    print ("  You are followed by %d users." % len(followers))
    diff = followings - followers
    print ("  %d users don't follow you back." % len(diff))
    bot.unfollow_users(list(diff))
