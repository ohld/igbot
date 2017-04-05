"""
    Bot's limits to prevent being banned.
"""

import datetime


def reset_counters(bot):
    bot.User.counters.likes = 0
    bot.User.counters.unlikes = 0
    bot.User.counters.followeds = 0
    bot.User.counters.unfollows = 0
    bot.User.counters.comments = 0
    bot.User.counters.blocks = 0
    bot.User.counters.unblocks = 0
    bot.start_time = datetime.datetime.now()


def reset_if_day_passed(bot):
    current_date = datetime.datetime.now()
    passed_days = (current_date.date() - bot.start_time.date()).days
    if passed_days != 0:
        reset_counters(bot)


def check_if_bot_can_follow(bot):
    reset_if_day_passed(bot)
    return bot.User.limits.max_follows_per_day - bot.User.counters.follows > 0


def check_if_bot_can_unfollow(bot):
    reset_if_day_passed(bot)
    return bot.User.limits.max_unfollows_per_day - bot.User.counters.unfollows > 0


def check_if_bot_can_unlike(bot):
    reset_if_day_passed(bot)
    return bot.User.limits.max_unlikes_per_day - bot.User.counters.unlikes > 0


def check_if_bot_can_like(bot):
    reset_if_day_passed(bot)
    return bot.User.limits.max_likes_per_day - bot.User.counters.likes> 0


def check_if_bot_can_comment(bot):
    reset_if_day_passed(bot)
    return bot.User.limits.max_comments_per_day - bot.User.counters.comments > 0


def check_if_bot_can_block(bot):
    reset_if_day_passed(bot)
    return bot.User.limits.max_blocks_per_day - bot.User.counters.blocks > 0


def check_if_bot_can_unblock(bot):
    reset_if_day_passed(bot)
    return bot.User.limits.max_unblocks_per_day - bot.User.counters.unblocks > 0
