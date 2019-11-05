"""
    Watch user likers stories!
    This script could be very useful to attract someone's
    audience to your account.

    If you will not specify the user_id, the script will use
    your likers as targets.

    Dependencies:
        pip install -U instabot

    Notes:
        You can change file and add there your comments.
"""

import os
import random
import sys
import time

# in case if you just downloaded zip with sources
sys.path.append(os.path.join(sys.path[0], "../../"))
from instabot import Bot  # noqa: E402

bot = Bot()
bot.login()

if len(sys.argv) >= 2:
    bot.logger.info(
        """
            Going to get '%s' likers and watch their stories
            (and stories of their likers too).
        """
        % (sys.argv[1])
    )
    user_to_get_likers_of = bot.convert_to_user_id(sys.argv[1])
else:
    bot.logger.info(
        """
            Going to get your likers and watch their stories (and stories
            of their likers too). You can specify username of another user
            to start (by default we use you as a starting point).
        """
    )
    user_to_get_likers_of = bot.user_id

current_user_id = user_to_get_likers_of
while True:
    try:
        # GET USER FEED
        if not bot.api.get_user_feed(current_user_id):
            print("Can't get feed of user_id=%s" % current_user_id)

        # GET MEDIA LIKERS
        user_media = random.choice(bot.api.last_json["items"])
        if not bot.api.get_media_likers(media_id=user_media["pk"]):
            bot.logger.info(
                "Can't get media likers of media_id='%s' by user_id='%s'"
                % (user_media["id"], current_user_id)
            )

        likers = bot.api.last_json["users"]
        liker_ids = [
            str(u["pk"])
            for u in likers
            if not u["is_private"] and "latest_reel_media" in u
        ][:20]

        # WATCH USERS STORIES
        if bot.watch_users_reels(liker_ids):
            bot.logger.info(
                "Total stories viewed: %d" % bot.total["stories_viewed"]
            )

        # CHOOSE RANDOM LIKER TO GRAB HIS LIKERS AND REPEAT
        current_user_id = random.choice(liker_ids)

        if random.random() < 0.05:
            current_user_id = user_to_get_likers_of
            bot.logger.info(
                "Sleeping and returning back to original user_id=%s"
                % current_user_id
            )
            time.sleep(90 * random.random() + 60)

    except Exception as e:
        # If something went wrong - sleep long and start again
        bot.logger.info(e)
        current_user_id = user_to_get_likers_of
        time.sleep(240 * random.random() + 60)
