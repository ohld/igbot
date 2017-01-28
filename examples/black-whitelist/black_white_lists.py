"""
    instabot example

    Workflow:
        1) Reads user_ids from blacklist and whitelist

    Notes:
        blacklist and whitelist files should contain user_id - each one on the
        separate line.
        Example:
            1234125
            1234124512
"""

import sys
import os

sys.path.append(os.path.join(sys.path[0],'../../'))
from instabot import Bot
