from instabot import Bot
import requests
import os, sys
import argparse
sys.path.append(os.path.join(sys.path[0], '../'))
parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('username', type=str, help='@username')
args = parser.parse_args()
if args.username[0] != "@":  # if first character isn't "@"
    args.username = "@" + args.username

bot = Bot()
bot.login()

def download_stories(username):
    user_id = bot.get_user_id_from_username(username)
    stories = bot.get_user_stories(user_id)
    print(stories)

    if stories == []:
        bot.logger.error(
            "Make sure that '{}' is NOT private.".format(username))
        return

    bot.logger.info("Downloading stories...")
    for story_url in stories:
        if ".mp4" in story_url:
            filename = story_url.split('/')[-1].split('.')[0] + ".mp4"
        elif ".jpg" in story_url:
            filename = story_url.split('/')[-1].split('.')[0] + ".jpg"

        response = requests.get(story_url, stream=True)
        with open(filename, "wb") as handle:
            for data in response.iter_content():
                handle.write(data)


download_stories("") #INSERT USERNAME HERE
