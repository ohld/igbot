"""
    Work with
        whitelist, blacklist,
        seleb account,
"""

import os

def read_list(file_path):
    """
        Reads whitelist/blacklist users from input file.
        Returns the list if file items
    """
    try:
        if not os.path.exists(file_path):
            print ("file %s does not exist." % file_path)
            return False
        with open(file_path, "r") as f:
            content = f.readlines()
            content = [item.strip() for item in content if len(item.strip()) > 0]
            return content
    except:
        return False

def add_whitelist(bot, file_path):
    bot.whitelist = read_list(file_path)
    return not not bot.whitelist

def add_blacklist(bot, file_path):
    bot.blacklist = read_list(file_path)
    return not not bot.blacklist

def get_media_owner(bot, media_id):
    bot.mediaInfo(media_id)
    try:
        return bot.LastJson["items"][0]["user"]["pk"]
    except:
        return False

def check_media(bot, media_id):
    return check_user(bot, get_media_owner(bot, media_id))

def check_user(bot, user_id):
    """
        Decide should you interract with that user_id or not.
        Decision based on
            1) Following/followers ratio
            2) Approved account
            3) Black-whitelist
            4) Closed accs
    """
    if not user_id:
        return True
    if bot.whitelist:
        if user_id in bot.whitelist:
            return True
    if bot.blacklist:
        if user_id in bot.blacklist:
            return False
    return True
