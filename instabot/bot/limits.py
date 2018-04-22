"""
    Bot's limits to prevent being banned.
"""

import datetime


def reset_counters(bot):
    for k in bot.total:
        bot.total[k] = 0
    bot.start_time = datetime.datetime.now()


def reset_if_day_passed(bot):
    current_date = datetime.datetime.now()
    passed_days = (current_date.date() - bot.start_time.date()).days
    if passed_days > 1:
        reset_counters(bot)


def check_if_bot_can_follow(bot):
    reset_if_day_passed(bot)
    return bot.max_per_day['follows'] - bot.total['followed'] > 0


def check_if_bot_can_unfollow(bot):
    reset_if_day_passed(bot)
    return bot.max_per_day['unfollows'] - bot.total['unfollowed'] > 0


def check_if_bot_can_unlike(bot):
    reset_if_day_passed(bot)
    return bot.max_per_day['unlikes'] - bot.total['unliked'] > 0


def check_if_bot_can_like(bot):
    reset_if_day_passed(bot)
    return bot.max_per_day['likes'] - bot.total['liked'] > 0


def check_if_bot_can_comment(bot):
    reset_if_day_passed(bot)
    return bot.max_per_day['comments'] - bot.total['commented'] > 0


def check_if_bot_can_block(bot):
    reset_if_day_passed(bot)
    return bot.max_per_day['blocks'] - bot.total['blocked'] > 0


def check_if_bot_can_unblock(bot):
    reset_if_day_passed(bot)
    return bot.max_per_day['unblocks'] - bot.total['unblocked'] > 0


def check_if_bot_can_send_message(bot):
    reset_if_day_passed(bot)
    return bot.max_per_day['messages'] - bot.total['sent_messages'] > 0
