from __future__ import unicode_literals

import json
import os
import shutil
import time
from random import randint

from requests_toolbelt import MultipartEncoder

from . import config
from .api_photo import get_image_size, stories_shaper


def download_story(self, filename, story_url, username):
    path = "stories/{}".format(username)
    if not os.path.exists(path):
        os.makedirs(path)
    fname = os.path.join(path, filename)
    if os.path.exists(fname):  # already exists
        self.logger.info("Stories already downloaded...")
        return os.path.abspath(fname)
    response = self.session.get(story_url, stream=True)
    if response.status_code == 200:
        with open(fname, "wb") as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)
        return os.path.abspath(fname)


def upload_story_photo(self, photo, upload_id=None):
    if upload_id is None:
        upload_id = str(int(time.time() * 1000))
    photo = stories_shaper(photo)
    if not photo:
        return False

    with open(photo, "rb") as f:
        photo_bytes = f.read()

    data = {
        "upload_id": upload_id,
        "_uuid": self.uuid,
        "_csrftoken": self.token,
        "image_compression": '{"lib_name":"jt","lib_version":"1.3.0",'
        + 'quality":"87"}',
        "photo": (
            "pending_media_%s.jpg" % upload_id,
            photo_bytes,
            "application/octet-stream",
            {"Content-Transfer-Encoding": "binary"},
        ),
    }
    m = MultipartEncoder(data, boundary=self.uuid)
    self.session.headers.update(
        {
            "Accept-Encoding": "gzip, deflate",
            "Content-type": m.content_type,
            "Connection": "close",
            "User-Agent": self.user_agent,
        }
    )
    response = self.session.post(config.API_URL + "upload/photo/", data=m.to_string())

    if response.status_code == 200:
        upload_id = json.loads(response.text).get("upload_id")
        if self.configure_story(upload_id, photo):
            # self.expose()
            return True
    return False


def configure_story(self, upload_id, photo):
    (w, h) = get_image_size(photo)
    data = self.json_data(
        {
            "source_type": 4,
            "upload_id": upload_id,
            "story_media_creation_date": str(int(time.time()) - randint(11, 20)),
            "client_shared_at": str(int(time.time()) - randint(3, 10)),
            "client_timestamp": str(int(time.time())),
            "configure_mode": 1,  # 1 - REEL_SHARE, 2 - DIRECT_STORY_SHARE
            "device": self.device_settings,
            "edits": {
                "crop_original_size": [w * 1.0, h * 1.0],
                "crop_center": [0.0, 0.0],
                "crop_zoom": 1.3333334,
            },
            "extra": {"source_width": w, "source_height": h},
        }
    )
    return self.send_request("media/configure_to_story/?", data)
