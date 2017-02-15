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
        TODO: convert the print function to a logger
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

def add_whitelist(self, file_path):
    self.whitelist = read_list(file_path)
    return not not self.whitelist

def add_blacklist(self, file_path):
    self.blacklist = read_list(file_path)
    return not not self.blacklist

def get_media_owner(self, media_id):
    self.mediaInfo(media_id)
    try:
        return self.LastJson["items"][0]["user"]["pk"]
    except:
        return False

def check_media(self, media_id):
    return check_user(self, get_media_owner(self, media_id))

def check_user(self, user_id):
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
    if self.whitelist:
        if user_id in self.whitelist:
            return True
    if self.blacklist:
        if user_id in self.blacklist:
            return False
    return True
