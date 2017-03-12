"""
    Bot's limits to prevent being banned.
"""

import datetime


def reset_counters(bot):
    bot.total_liked = 0
    bot.total_unliked = 0
    bot.total_followed = 0
    bot.total_unfollowed = 0
    bot.total_commented = 0
    bot.total_blocked = 0
    bot.total_unblocked = 0
    bot.start_time = datetime.datetime.now()


def reset_if_day_passed(bot):
    passed_seconds = (datetime.datetime.now() - bot.start_time).total_seconds()
    if passed_seconds > 60*60*24:
        reset_counters(bot)


def check_if_bot_can_follow(bot):
    reset_if_day_passed(bot)
    return bot.max_follows_per_day - bot.total_followed > 0


def check_if_bot_can_unfollow(bot):
    reset_if_day_passed(bot)
    return bot.max_unfollows_per_day - bot.total_unfollowed > 0


def check_if_bot_can_unlike(bot):
    reset_if_day_passed(bot)
    return bot.max_unlikes_per_day - bot.total_unliked > 0


def check_if_bot_can_like(bot):
    reset_if_day_passed(bot)
    return bot.max_likes_per_day - bot.total_liked > 0


def check_if_bot_can_comment(bot):
    reset_if_day_passed(bot)
    return bot.max_comments_per_day - bot.total_commented > 0


def check_if_bot_can_block(bot):
    reset_if_day_passed(bot)
    return bot.max_blocks_per_day - bot.total_blocked > 0


def check_if_bot_can_unblock(bot):
    reset_if_day_passed(bot)
    return bot.max_unblocks_per_day - bot.total_unblocked > 0
