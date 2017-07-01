"""
    Support instabot's methods.
"""

import sys
import os
import codecs


def check_if_file_exists(file_path):
    if not os.path.exists(file_path):
        if not quiet:
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


def check_whitelists(self):

    """
        Check whitelists in folder with script
    """

    default_names = ('whitelist.txt',
                     'friends_{0}.txt'.format(self.username),
                     'friends_{0}.txt'.format(self.user_id),
                     'friends.txt')

    for file_path in default_names:
        whitelist = read_list_from_file(file_path)
        if whitelist:
            self.logger.info('Found whitelist: {0} ({1} users)'.format(file_path, len(whitelist)))
            return whitelist
    return []


def check_dont_follows(self):

    """
        Check don't_follow in folder with script
    """

    default_names = ('dontFollow.txt',
                     '')

    for file_path in default_names:
        dont_follow = read_list_from_file(file_path)
        if dont_follow:
            self.logger.info('Found dontFollow: {0} ({1} users)'.format(file_path, len(dont_follow)))
            return dont_follow
    return []


def add_whitelist(self, file_path):
    file_contents = read_list_from_file(file_path)
    self.whitelist = [self.convert_to_user_id(item) for item in file_contents]
    return not not self.whitelist


def add_blacklist(self, file_path):
    file_contents = read_list_from_file(file_path)
    self.blacklist = [self.convert_to_user_id(item) for item in file_contents]
    return not not self.blacklist


def add_dont_follow(self, file_path):
    file_contents = read_list_from_file(file_path)
    self.dont_follow = [self.convert_to_user_id(item) for item in file_contents]
    return not not self.dont_follow
