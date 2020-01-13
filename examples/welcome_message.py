"""
instabot example
Workflow:
Welcome message for new followers.
"""
import argparse
import datetime
import os
import sys
import time


sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot  # noqa: E402

RETRY_DELAY = 60
DELAY = 30 * 60


def get_recent_followers(bot, from_time):
    followers = []
    ok = bot.api.get_recent_activity()
    if not ok:
        raise ValueError("failed to get activity")
    activity = bot.api.last_json
    for feed in [activity["new_stories"], activity["old_stories"]]:
        for event in feed:
            if event.get("args", {}).get("text", "").endswith("started following you."):
                follow_time = datetime.datetime.utcfromtimestamp(
                    event["args"]["timestamp"]
                )
                if follow_time < from_time:
                    continue
                followers.append(
                    {
                        "user_id": event["args"]["profile_id"],
                        "username": event["args"]["profile_name"],
                        "follow_time": follow_time,
                    }
                )
    return followers


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("-u", type=str, help="username")
    parser.add_argument("-p", type=str, help="password")
    parser.add_argument("-proxy", type=str, help="proxy")
    parser.add_argument(
        "-message",
        type=str,
        nargs="?",
        help="message text",
        default="Hi, thanks for reaching me",
    )
    args = parser.parse_args()

    bot = Bot()
    bot.login(username=args.u, password=args.p, proxy=args.proxy)

    start_time = datetime.datetime.utcnow()

    while True:
        try:
            new_followers = get_recent_followers(bot, start_time)
        except ValueError as err:
            print(err)
            time.sleep(RETRY_DELAY)
            continue

        if new_followers:
            print(
                "Found new followers. Count: {count}".format(count=len(new_followers))
            )

        for follower in new_followers:
            print("New follower: {}".format(follower["username"]))
            bot.send_message(args.message, str(follower["user_id"]))

        start_time = datetime.datetime.utcnow()
        time.sleep(DELAY)


if __name__ == "__main__":
    main()
