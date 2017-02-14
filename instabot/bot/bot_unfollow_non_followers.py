import time
import random
import json

def unfollow_non_followers(bot):
  followings = set([item["pk"] for item in bot.getTotalSelfFollowings()])
  bot.logger.info("Unfollowing non-followers")
  bot.logger.info("  You follow %d users." % len(followings))
  followers = set([item["pk"] for item in bot.getTotalSelfFollowers()])
  bot.logger.info("  You are followed by %d users." % len(followers))
  diff = followings - followers
  bot.logger.info("  %d users don't follow you back." % len(diff))
  bot.unfollow_users(list(diff))
