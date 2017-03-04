"""

"""

import os
import io


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
        with io.open(file_path, "r", encoding="utf8") as f:
            content = f.readlines()
            content = [str(item.strip())
                       for item in content if len(item.strip()) > 0]
            return content
    except:
        return []


def add_whitelist(self, file_path):
    file_contents = read_list_from_file(file_path)
    self.whitelist = [self.convert_to_user_id(item) for item in file_contents]
    return not not self.whitelist


def add_blacklist(self, file_path):
    file_contents = read_list_from_file(file_path)
    self.blacklist = [self.convert_to_user_id(item) for item in file_contents]
    return not not self.blacklist
