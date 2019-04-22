from __future__ import unicode_literals
import imghdr
import os
import shutil
import struct
import time

from requests_toolbelt import MultipartEncoder

from . import config

def download_story(self, filename, story_url, username):

    p = "stories/" + username
    if not os.path.exists(p):
        os.makedirs(p)
    fname = os.path.join(p, filename)
    if os.path.exists(fname):  # already exists
        print("Stories already downloaded...")
        return os.path.abspath(fname)
    response = self.session.get(story_url, stream=True)
    if response.status_code == 200:
        with open(fname, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)
        return os.path.abspath(fname)
