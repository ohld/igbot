"""
    Bot's limits to prevent being banned.
"""

import datetime

MAX_LIKES_PER_DAY = 1000
MAX_FOLLOWS_PER_DAY = 350
MAX_UNFOLLOWS_PER_DAY = 350
MAX_COMMENTS_PER_DAY = 100
MAX_LIKES_TO_LIKE = 80

def reset_counters(bot):
    bot.total_liked = 0
    bot.total_unliked = 0
    bot.total_followed = 0
    bot.total_unfollowed = 0
    bot.total_commented = 0

def reset_if_day_passed(bot):
    current_date = datetime.datetime.now()
    passed_days = (current_date.date() - bot.start_time.date()).days
    if passed_days != 0:
        reset_counters(bot)

def check_if_bot_can_follow(bot):
    reset_if_day_passed(bot)
    return bot.max_follows_per_day - bot.total_followed > 0

def check_if_bot_can_like(bot):
    reset_if_day_passed(bot)
    return bot.max_likes_per_day - bot.total_liked > 0

def check_if_bot_can_comment(bot):
    reset_if_day_passed(bot)
    return bot.max_comments_per_day - bot.total_commented > 0
