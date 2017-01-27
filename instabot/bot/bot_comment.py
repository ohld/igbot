"""
    Bot functions to generate and post a comments.

    Instructions to file with comments:
        one line - one comment.

    Example:
        lol
        kek

"""

import random
import os
import io

def get_random_comment_from_file(file_path):
    with io.open(file_path, "r", encoding="utf8") as f:
        content = f.readlines()
        return random.choice(content).strip()

def get_comment(bot, comment_base_file=None):
    """
        Generates comment.
        If comment_base_file argunment is passed, it uses the lines from file
        as comments to return.

        TODO: generate more way to create comments.
    """
    if comment_base_file is not None:
        if os.path.exists(comment_base_file):
            return get_random_comment_from_file(comment_base_file)
        else:
            print ("Can't find your file with comments.")
            return "lol"
    else:
        return "lol"
