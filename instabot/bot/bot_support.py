"""
    Support instabot's methods.
"""

import sys
import os
import codecs


def check_if_file_exists(file_path):
    if not os.path.exists(file_path):
        print("Can't find '%s' file." % file_path)
        return False
    return True


def read_list_from_file(file_path):
    """
        Reads list from file. One line - one item.
        Returns the list if file items.
    """
    try:
        if not check_if_file_exists(file_path):
            return []
        with codecs.open(file_path, "r", encoding="utf-8") as f:
            content = f.readlines()
            if sys.version_info[0] < 3:
                content = [str(item.encode('utf8')) for item in content]
            content = [item.strip() for item in content if len(item) > 0]
            return content
    except Exception as e:
        print(str(e))
        return []


def add_whitelist(self, file_path):
    file_contents = read_list_from_file(file_path)
    self.whitelist = [self.convert_to_user_id(item) for item in file_contents]
    return not not self.whitelist


def add_blacklist(self, file_path):
    file_contents = read_list_from_file(file_path)
    self.blacklist = [self.convert_to_user_id(item) for item in file_contents]
    return not not self.blacklist
