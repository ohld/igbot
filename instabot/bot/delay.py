"""
    Function to calculate delays for like/follow/unfollow etc.
"""

import random
import time


def add_dispersion(delay_value):
    return delay_value * random.uniform(0.25, 1.25)


# this function will sleep only if elapsed time since `last_action` is less than `target_delay`
def sleep_if_need(bot, key):
    last_action, target_delay = bot.last[key], bot.delay[key]
    now = time.time()
    elapsed_time = now - last_action
    if elapsed_time < target_delay:
        remains_to_wait = target_delay - elapsed_time
        time.sleep(add_dispersion(remains_to_wait))
    bot.last[key] = time.time()


def like_delay(bot):
    sleep_if_need(bot, 'like')


def message_delay(bot):
    sleep_if_need(bot, 'message')


def unlike_delay(bot):
    sleep_if_need(bot, 'unlike')


def follow_delay(bot):
    sleep_if_need(bot, 'follow')


def unfollow_delay(bot):
    sleep_if_need(bot, 'unfollow')


def comment_delay(bot):
    sleep_if_need(bot, 'comment')


def block_delay(bot):
    sleep_if_need(bot, 'block')


def unblock_delay(bot):
    sleep_if_need(bot, 'unblock')


def error_delay(bot):
    time.sleep(10)


def delay_in_seconds(bot, delay_time=60):
    time.sleep(delay_time)


def small_delay(bot):
    time.sleep(add_dispersion(3))


def very_small_delay(bot):
    time.sleep(add_dispersion(0.7))
