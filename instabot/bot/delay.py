"""
    Function to calculate delays for like/follow/unfollow etc.
"""

import time
import random


def add_dispersion(delay_value):
    return delay_value * 3 / 4 + delay_value * random.random() / 2


def sleep(t):
    time.sleep(add_dispersion(t))


def like_delay(bot):
    sleep(bot.User.delays.like)


def unlike_delay(bot):
    sleep(bot.User.delays.unlike)


def follow_delay(bot):
    sleep(bot.User.delays.follow)


def unfollow_delay(bot):
    sleep(bot.User.delays.unfollow)


def comment_delay(bot):
    sleep(bot.User.delays.comment)


def block_delay(bot):
    sleep(bot.User.delays.block)


def unblock_delay(bot):
    sleep(bot.User.delays.unblock)


def error_delay(bot):
    sleep(10)


def small_delay(bot):
    sleep(3)


def very_small_delay(bot):
    sleep(0.7)
