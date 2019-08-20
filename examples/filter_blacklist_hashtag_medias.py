"""
    instabot filters out the media with your set blacklist hashtags

    Workflow:
        Try to follow a media with your blacklist hashtag in the
        description and see how bot filters it out.
"""

import os
import sys

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot

blacklist_hashtag_input = input("\n Enter a blacklist hashtag: ")

bot = Bot(
    filter_users=True,
    filter_private_users=True,
    filter_previously_followed=True,
    filter_business_accounts=True,
    filter_verified_accounts=True,
    blacklist_hashtags=[blacklist_hashtag_input],
)
bot.login()
bot.like_hashtag(blacklist_hashtag_input, amount=2)
