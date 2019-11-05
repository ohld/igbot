# -*- coding: utf-8 -*-
import copy
import json
import os
import re
import shutil
import subprocess
import time

from requests_toolbelt import MultipartEncoder

from . import config


def download_video(
    self,
    media_id,
    filename=None,
    media=False,
    folder="videos"
):
    video_urls = []
    if not media:
        self.media_info(media_id)
        media = self.last_json["items"][0]
    filename = (
        "{}_{}.mp4".format(media["user"]["username"], media_id)
        if not filename
        else "{}.mp4".format(filename)
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

    fname = os.path.join(folder, filename)
    if os.path.exists(fname):
        return os.path.abspath(fname)

    for counter, video_url in enumerate(video_urls):
        response = self.session.get(video_url, stream=True)
        if response.status_code == 200:
            fname = os.path.join(folder, "{}_{}".format(counter, filename))
            with open(fname, "wb") as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)

    return os.path.abspath(fname)


# leaving here function used by old upload_video, no more used now
def get_video_info(filename):
    res = {}
    try:
        terminalResult = subprocess.Popen(
            ["ffprobe", filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        for x in terminalResult.stdout.readlines():
            # Duration: 00:00:59.51, start: 0.000000, bitrate: 435 kb/s
            m = re.search(
                r"duration: (\d\d:\d\d:\d\d\.\d\d),",
                str(x),
                flags=re.IGNORECASE
            )
            if m is not None:
                res["duration"] = m.group(1)
            # Video: h264 (Constrained Baseline)
            # (avc1 / 0x31637661), yuv420p, 480x268
            m = re.search(
                r"video:\s.*\s(\d+)x(\d+)\s",
                str(x),
                flags=re.IGNORECASE
            )
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


def upload_video(
    self,
    video,
    caption=None,
    upload_id=None,
    thumbnail=None,
    options={}
):
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
    data = {
        "upload_id": upload_id,
        "_csrftoken": self.token,
        "media_type": "2",
        "_uuid": self.uuid,
    }
    m = MultipartEncoder(data, boundary=self.uuid)
    self.session.headers.update(
        {
            "X-IG-Capabilities": "3Q4=",
            "X-IG-Connection-Type": "WIFI",
            "Host": "i.instagram.com",
            "Cookie2": "$Version=1",
            "Accept-Language": "en-US",
            "Accept-Encoding": "gzip, deflate",
            "Content-type": m.content_type,
            "Connection": "keep-alive",
            "User-Agent": self.user_agent,
        }
    )
    response = self.session.post(
        config.API_URL + "upload/video/", data=m.to_string()
    )
    if response.status_code == 200:
        body = json.loads(response.text)
        upload_url = body["video_upload_urls"][3]["url"]
        upload_job = body["video_upload_urls"][3]["job"]

        with open(video, "rb") as video_bytes:
            video_data = video_bytes.read()
        # solve issue #85 TypeError:
        # slice indices must be integers or None or have an __index__ method
        request_size = len(video_data) // 4
        last_request_extra = len(video_data) - 3 * request_size

        headers = copy.deepcopy(self.session.headers)
        self.session.headers.update(
            {
                "X-IG-Capabilities": "3Q4=",
                "X-IG-Connection-Type": "WIFI",
                "Cookie2": "$Version=1",
                "Accept-Language": "en-US",
                "Accept-Encoding": "gzip, deflate",
                "Content-type": "application/octet-stream",
                "Session-ID": upload_id,
                "Connection": "keep-alive",
                "Content-Disposition": 'attachment; filename="video.mov"',
                "job": upload_job,
                "Host": "upload.instagram.com",
                "User-Agent": self.user_agent,
            }
        )
        for i in range(4):
            start = i * request_size
            if i == 3:
                end = i * request_size + last_request_extra
            else:
                end = (i + 1) * request_size
            length = last_request_extra if i == 3 else request_size
            content_range = "bytes {start}-{end}/{len_video}".format(
                start=start, end=end - 1, len_video=len(video_data)
            ).encode("utf-8")

            self.session.headers.update(
                {
                    "Content-Length": str(end - start),
                    "Content-Range": content_range
                }
            )
            response = self.session.post(
                upload_url, data=video_data[start: start + length]
            )
        self.session.headers = headers

        configure_timeout = options.get("configure_timeout")
        if response.status_code == 200:
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
                        from os import rename

                        rename(video, "{}.REMOVE_ME".format(video))
                    return media
    return False


def configure_video(
    self,
    upload_id,
    video,
    thumbnail,
    width,
    height,
    duration,
    caption="",
    options={}
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
    # clipInfo = get_video_info(video)
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
            "source_type": 3,
            "poster_frame_index": 0,
            "length": 0.00,
            "audio_muted": False,
            "filter_type": 0,
            "video_result": "deprecated",
            "clips": {
                "length": duration,
                "source_type": "3",
                "camera_position": "back",
            },
            "extra": {"source_width": width, "source_height": height},
            "device": self.device_settings,
            "caption": caption,
        }
    )
    return self.send_request("media/configure/?video=1", data)


def resize_video(fname, thumbnail=None):
    from math import ceil

    try:
        import moviepy.editor as mp
    except ImportError as e:
        print("ERROR: {}".format(e))
        print(
            "Required module `moviepy` not installed\n"
            "Install with `pip install moviepy` and retry.\n\n"
            "You may need also:\n"
            "pip install --upgrade setuptools\n"
            "pip install numpy --upgrade --ignore-installed"
        )
        return False
    print("Analizing `{}`".format(fname))
    h_lim = {"w": 90.0, "h": 47.0}
    v_lim = {"w": 4.0, "h": 5.0}
    d_lim = 60
    vid = mp.VideoFileClip(fname)
    (w, h) = vid.size
    deg = vid.rotation
    ratio = w * 1.0 / h * 1.0
    print(
        "FOUND w:{w}, h:{h}, rotation={d}, ratio={r}".format(
            w=w,
            h=h,
            r=ratio,
            d=deg
        )
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
        if w > 1080:
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
        if h > 1080:
            print("Resizing video")
            vid = vid.resize(height=1080)
    else:
        print("Square video")
        if w > 1080:
            print("Resizing video")
            vid = vid.resize(width=1080)
    (w, h) = vid.size
    if vid.duration > d_lim:
        print("Cutting video to {} sec from start".format(d_lim))
        vid = vid.subclip(0, d_lim)
    new_fname = "{}.CONVERTED.mp4".format(fname)
    print(
        "Saving new video w:{w} h:{h} to `{f}`".format(
            w=w,
            h=h,
            f=new_fname
        )
    )
    vid.write_videofile(new_fname, codec="libx264", audio_codec="aac")
    if not thumbnail:
        print("Generating thumbnail...")
        thumbnail = "{}.jpg".format(fname)
        vid.save_frame(thumbnail, t=(vid.duration / 2))
    return new_fname, thumbnail, w, h, vid.duration
