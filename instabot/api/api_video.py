from __future__ import unicode_literals

import json
import os
import re
import shutil
import subprocess
import time
import random
from uuid import uuid4

from . import config


def download_video(self, media_id, filename=None, media=False, folder="videos"):
    video_urls = []
    if not media:
        self.media_info(media_id)
        try:
            media = self.last_json["items"][0]
        except IndexError:
            raise Exception("Media (media_id=%s) not found for download" % media_id)
    filename = (
        "{username}_{media_id}.mp4".format(
            username=media["user"]["username"], media_id=media_id
        )
        if not filename
        else "{fname}.mp4".format(fname=filename)
    )

    try:
        clips = media["video_versions"]
        video_urls.append(clips[0]["url"])
    except KeyError:
        carousels = media.get("carousel_media", [])
        for carousel in carousels:
            video_urls.append(carousel["video_versions"][0]["url"])
    except Exception:
        return False

    for counter, video_url in enumerate(video_urls):
        fname = os.path.join(
            folder, "{cnt}_{fname}".format(cnt=counter, fname=filename)
        )
        if os.path.exists(fname):
            print("File %s is exists, return it" % fname)
            return os.path.abspath(fname)
        response = self.session.get(video_url, stream=True)
        if response.status_code == 200:
            with open(fname, "wb") as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)

    return os.path.abspath(fname)


# leaving here function used by old upload_video, no more used now
def get_video_info(filename):
    res = {}
    try:
        terminalResult = subprocess.Popen(
            ["ffprobe", filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        for x in terminalResult.stdout.readlines():
            # Duration: 00:00:59.51, start: 0.000000, bitrate: 435 kb/s
            m = re.search(
                r"duration: (\d\d:\d\d:\d\d\.\d\d),", str(x), flags=re.IGNORECASE
            )
            if m is not None:
                res["duration"] = m.group(1)
            # Video: h264 (Constrained Baseline)
            # (avc1 / 0x31637661), yuv420p, 480x268
            m = re.search(r"video:\s.*\s(\d+)x(\d+)\s", str(x), flags=re.IGNORECASE)
            if m is not None:
                res["width"] = m.group(1)
                res["height"] = m.group(2)
    finally:
        if "width" not in res:
            print(
                "ERROR: 'ffprobe' not found, please install "
                "'ffprobe' with one of following methods:"
            )
            print("   sudo apt-get install ffmpeg")
            print("or sudo apt-get install -y libav-tools")
    return res


def upload_video(self, video, caption=None, upload_id=None, thumbnail=None, options={}):
    """Upload video to Instagram

    @param video      Path to video file (String)
    @param caption    Media description (String)
    @param upload_id  Unique upload_id (String). When None, then generate
                      automatically
    @param thumbnail  Path to thumbnail for video (String). When None, then
                      thumbnail is generate automatically
    @param options    Object with difference options, e.g. configure_timeout,
                      rename_thumbnail, rename (Dict)
                      Designed to reduce the number of function arguments!
                      This is the simplest request object.

    @return           Object with state of uploading to Instagram (or False)
    """
    options = dict(
        {"configure_timeout": 15, "rename_thumbnail": True, "rename": True},
        **(options or {})
    )
    if upload_id is None:
        upload_id = str(int(time.time() * 1000))
    video, thumbnail, width, height, duration = resize_video(video, thumbnail)
    waterfall_id = str(uuid4())
    # upload_name example: '1576102477530_0_7823256191'
    upload_name = "{upload_id}_0_{rand}".format(
        upload_id=upload_id, rand=random.randint(1000000000, 9999999999)
    )
    rupload_params = {
        "retry_context": '{"num_step_auto_retry":0,"num_reupload":0,"num_step_manual_retry":0}',
        "media_type": "2",
        "xsharing_user_ids": "[]",
        "upload_id": upload_id,
        "upload_media_duration_ms": str(int(duration * 1000)),
        "upload_media_width": str(width),
        "upload_media_height": str(height),
    }
    self.session.headers.update(
        {
            "Accept-Encoding": "gzip",
            "X-Instagram-Rupload-Params": json.dumps(rupload_params),
            "X_FB_VIDEO_WATERFALL_ID": waterfall_id,
            "X-Entity-Type": "video/mp4",
        }
    )
    response = self.session.get(
        "https://{domain}/rupload_igvideo/{name}".format(
            domain=config.API_DOMAIN, name=upload_name
        )
    )
    if response.status_code != 200:
        return False
    video_data = open(video, "rb").read()
    video_len = str(len(video_data))
    self.session.headers.update(
        {
            "Offset": "0",
            "X-Entity-Name": upload_name,
            "X-Entity-Length": video_len,
            "Content-Type": "application/octet-stream",
            "Content-Length": video_len,
        }
    )
    response = self.session.post(
        "https://{domain}/rupload_igvideo/{name}".format(
            domain=config.API_DOMAIN, name=upload_name
        ),
        data=video_data,
    )
    if response.status_code != 200:
        return False
    # CONFIGURE
    configure_timeout = options.get("configure_timeout")
    for attempt in range(4):
        if configure_timeout:
            time.sleep(configure_timeout)
        if self.configure_video(
            upload_id,
            video,
            thumbnail,
            width,
            height,
            duration,
            caption,
            options=options,
        ):
            media = self.last_json.get("media")
            self.expose()
            if options.get("rename"):
                os.rename(video, "{fname}.REMOVE_ME".format(fname=video))
            return media
    return False


def configure_video(
    self, upload_id, video, thumbnail, width, height, duration, caption="", options={}
):
    """Post Configure Video (send caption, thumbnail and more to Instagram)

    @param upload_id  Unique upload_id (String). Received from "upload_video"
    @param video      Path to video file (String)
    @param thumbnail  Path to thumbnail for video (String). When None,
                      then thumbnail is generate automatically
    @param width      Width in px (Integer)
    @param height     Height in px (Integer)
    @param duration   Duration in seconds (Integer)
    @param caption    Media description (String)
    @param options    Object with difference options, e.g. configure_timeout,
                      rename_thumbnail, rename (Dict)
                      Designed to reduce the number of function arguments!
                      This is the simplest request object.
    """
    options = {"rename": options.get("rename_thumbnail", True)}
    self.upload_photo(
        photo=thumbnail,
        caption=caption,
        upload_id=upload_id,
        from_video=True,
        options=options,
    )
    data = self.json_data(
        {
            "upload_id": upload_id,
            "source_type": 4,
            "poster_frame_index": 0,
            "length": duration,
            "audio_muted": False,
            "filter_type": 0,
            "date_time_original": time.strftime("%Y:%m:%d %H:%M:%S", time.localtime()),
            "timezone_offset": "10800",
            "width": width,
            "height": height,
            "clips": [{"length": duration, "source_type": "4"}],
            "extra": {"source_width": width, "source_height": height},
            "device": self.device_settings,
            "caption": caption,
        }
    )
    return self.send_request("media/configure/?video=1", data, with_signature=True)


def resize_video(fname, thumbnail=None):
    from math import ceil

    try:
        import moviepy.editor as mp
    except ImportError as e:
        print("ERROR: {err}".format(err=e))
        print(
            "Required module `moviepy` not installed\n"
            "Install with `pip install moviepy` and retry.\n\n"
            "You may need also:\n"
            "pip install --upgrade setuptools\n"
            "pip install numpy --upgrade --ignore-installed"
        )
        return False
    print("Analizing `{fname}`".format(fname=fname))
    h_lim = {"w": 90.0, "h": 47.0}
    v_lim = {"w": 4.0, "h": 5.0}
    d_lim = 60
    vid = mp.VideoFileClip(fname)
    (w, h) = vid.size
    deg = vid.rotation
    ratio = w * 1.0 / h * 1.0
    print(
        "FOUND w:{w}, h:{h}, rotation={d}, ratio={r}".format(w=w, h=h, r=ratio, d=deg)
    )
    if w > h:
        print("Horizontal video")
        if ratio > (h_lim["w"] / h_lim["h"]):
            print("Cropping video")
            cut = int(ceil((w - h * h_lim["w"] / h_lim["h"]) / 2))
            left = cut
            right = w - cut
            top = 0
            bottom = h
            vid = vid.crop(x1=left, y1=top, x2=right, y2=bottom)
            (w, h) = vid.size
        if w > 1081:
            print("Resizing video")
            vid = vid.resize(width=1080)
    elif w < h:
        print("Vertical video")
        if ratio < (v_lim["w"] / v_lim["h"]):
            print("Cropping video")
            cut = int(ceil((h - w * v_lim["h"] / v_lim["w"]) / 2))
            left = 0
            right = w
            top = cut
            bottom = h - cut
            vid = vid.crop(x1=left, y1=top, x2=right, y2=bottom)
            (w, h) = vid.size
        if h > 1081:
            print("Resizing video")
            vid = vid.resize(height=1080)
    else:
        print("Square video")
        if w > 1081:
            print("Resizing video")
            vid = vid.resize(width=1080)
    (w, h) = vid.size
    return fname, thumbnail, w, h, vid.duration
    if vid.duration > d_lim:
        print("Cutting video to {lim} sec from start".format(lim=d_lim))
        vid = vid.subclip(0, d_lim)
    new_fname = "{fname}.CONVERTED.mp4".format(fname=fname)
    print("Saving new video w:{w} h:{h} to `{f}`".format(w=w, h=h, f=new_fname))
    vid.write_videofile(new_fname, codec="libx264", audio_codec="aac")
    if not thumbnail:
        print("Generating thumbnail...")
        thumbnail = "{fname}.jpg".format(fname=fname)
        vid.save_frame(thumbnail, t=(vid.duration / 2))
    return new_fname, thumbnail, w, h, vid.duration
