# -*- coding: utf-8 -*-

BLACKLIST_FILE = "blacklist.txt"  # List of the users you don't want to follow

WHITELIST_FILE = "whitelist.txt"  # List of users you don't want to unfollow

COMMENTS_FILE = "comments.txt"  # Contains random comments posted by the bot

FRIENDS_FILE = "friends.txt"  # Users IDs of friends

PHOTO_CAPTIONS_FILE = "photo_captions.txt"  # Captions to put under the photos

HASHTAGS_FILE = "hashtag_database.txt"
# The file containing hashtags you want to track: the bot will like and comment
# photos and follow users using the hashtags in this file

USERS_FILE = "username_database.txt"
# Same as HASHTAGS_FILE, but with users. The bot will follow those users'
# followers and like their posts

POSTED_PICS_FILE = "pics.txt"
# File containing all the photos already posted from the PICS_PATH directory

PICS_PATH = "/Path/to/pics/folder/"
# The path of the directory containing the photos the bot will upload
# NOTE: Being a directory, it must end with '/'

PICS_HASHTAGS = (
    "#hashtag1 #hashtag2 #hashtag3 #hashtag4 " "#hashtag5 #hashtag6 #hashtag7"
)
# The bot will comment each photo it posts with the hashtags in PICS_HASHTAGS
# Each string but the last must end with a space
# NOTE: Instagram allows only for a maximum of 30 hashtags per post.

FOLLOW_MESSAGE = "Follow @my_account for the best photos!"
# The string to insert under the random caption. The bot will construct each
# photo caption like the following ->
# [random caption taken from PHOTO_CAPTIONS]
# FOLLOW_MESSAGE

NUMBER_OF_FOLLOWERS_TO_FOLLOW = 15
# Specifies the number of people to follow each time the function
# bot.follow_followers gets executed. By default, this function gets
# executed by the bot every 2 days at 11:00.

NUMBER_OF_NON_FOLLOWERS_TO_UNFOLLOW = 50
# Specifies the number of people to unfollow each time the function
# bot.unfollow_non_followers gets executed. By default, this function
# gets executed every day at 08:00.

# NOTE: Because the bot follows a bunch of people through job7 (follow
# people by a random hashtag in HASHTAGS_FILE), I recommend setting
# NUMBER_OF_FOLLOWERS_TO_FOLLOW between 15 and 30, and
# NUMBER_OF_NON_FOLLOWERS_TO_UNFOLLOW between 50 and 60. Following and
# unfollowing many people in the same day can cause a temporary
# "follow ban" by Instagram: basically you can't follow or unfollow
# anybody for 24 hours.
