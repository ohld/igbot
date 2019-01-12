# -*- coding: utf-8 -*-
import copy
import json
import os
import re
import shutil
import subprocess
import time

from subprocess import Popen, PIPE
from requests_toolbelt import MultipartEncoder

from . import config


def download_video(self, media_id, filename, media=False, folder='videos'):
    if not media:
        self.media_info(media_id)
        media = self.last_json['items'][0]
    filename = '{0}_{1}.mp4'.format(media['user']['username'], media_id) if not filename else '{0}.mp4'.format(filename)
    try:
        clips = media['video_versions']
    except Exception:
        return False
    fname = os.path.join(folder, filename)
    if os.path.exists(fname):
        return os.path.abspath(fname)
    response = self.session.get(clips[0]['url'], stream=True)
    if response.status_code == 200:
        with open(fname, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)
        return os.path.abspath(fname)


def get_video_info(filename):
    res = {}
    try:
        terminalResult = subprocess.Popen(["ffprobe", filename],
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.STDOUT)
        for x in terminalResult.stdout.readlines():
            # Duration: 00:00:59.51, start: 0.000000, bitrate: 435 kb/s
            m = re.search(r'duration: (\d\d:\d\d:\d\d\.\d\d),', str(x), flags=re.IGNORECASE)
            if m is not None:
                res['duration'] = m.group(1)
            # Video: h264 (Constrained Baseline) (avc1 / 0x31637661), yuv420p, 480x268
            m = re.search(r'video:\s.*\s(\d+)x(\d+)\s', str(x), flags=re.IGNORECASE)
            if m is not None:
                res['width'] = m.group(1)
                res['height'] = m.group(2)
    finally:
        if 'width' not in res:
            print(("ERROR: 'ffprobe' not found, please install "
                   "'ffprobe' with one of following methods:"))
            print("   sudo apt-get install ffmpeg")
            print("or sudo apt-get install -y libav-tools")
    return res


def upload_video(self, video, caption=None, upload_id=None, thumbnail=None):
    from distutils.spawn import find_executable
    requirements = ['ffprobe', 'ffmpeg', 'convert']
    for requirement in requirements:
        if requirement == 'convert' and thumbnail is not None:
            continue
        if find_executable(requirement) is None:
            self.logger.error("{} not found in your OS. Please install and retry".format(requirement))
            return False
    if upload_id is None:
        upload_id = str(int(time.time() * 1000))
    if thumbnail is None:
        thumbnail = self.resize_video(video)
    if not thumbnail:
        self.logger.error("Error creating thumbnail...")
        return False
    data = {
        'upload_id': upload_id,
        '_csrftoken': self.token,
        'media_type': '2',
        '_uuid': self.uuid,
    }
    m = MultipartEncoder(data, boundary=self.uuid)
    self.session.headers.update({'X-IG-Capabilities': '3Q4=',
                                 'X-IG-Connection-Type': 'WIFI',
                                 'Host': 'i.instagram.com',
                                 'Cookie2': '$Version=1',
                                 'Accept-Language': 'en-US',
                                 'Accept-Encoding': 'gzip, deflate',
                                 'Content-type': m.content_type,
                                 'Connection': 'keep-alive',
                                 'User-Agent': self.user_agent})
    response = self.session.post(config.API_URL + "upload/video/", data=m.to_string())
    if response.status_code == 200:
        body = json.loads(response.text)
        upload_url = body['video_upload_urls'][3]['url']
        upload_job = body['video_upload_urls'][3]['job']

        with open(video, 'rb') as video_bytes:
            video_data = video_bytes.read()
        # solve issue #85 TypeError: slice indices must be integers or None or have an __index__ method
        request_size = len(video_data) // 4
        last_request_extra = len(video_data) - 3 * request_size

        headers = copy.deepcopy(self.session.headers)
        self.session.headers.update({
            'X-IG-Capabilities': '3Q4=',
            'X-IG-Connection-Type': 'WIFI',
            'Cookie2': '$Version=1',
            'Accept-Language': 'en-US',
            'Accept-Encoding': 'gzip, deflate',
            'Content-type': 'application/octet-stream',
            'Session-ID': upload_id,
            'Connection': 'keep-alive',
            'Content-Disposition': 'attachment; filename="video.mov"',
            'job': upload_job,
            'Host': 'upload.instagram.com',
            'User-Agent': self.user_agent
        })
        for i in range(4):
            start = i * request_size
            if i == 3:
                end = i * request_size + last_request_extra
            else:
                end = (i + 1) * request_size
            length = last_request_extra if i == 3 else request_size
            content_range = "bytes {start}-{end}/{len_video}".format(
                start=start, end=end - 1, len_video=len(video_data)).encode('utf-8')

            self.session.headers.update({'Content-Length': str(end - start), 'Content-Range': content_range})
            response = self.session.post(upload_url, data=video_data[start:start + length])
        self.session.headers = headers

        if response.status_code == 200:
            if self.configure_video(upload_id, video, thumbnail, caption):
                self.expose()
                return True
    return False


def configure_video(self, upload_id, video, thumbnail, caption=''):
    clipInfo = get_video_info(video)
    self.upload_photo(photo=thumbnail, caption=caption, upload_id=upload_id)
    data = self.json_data({
        'upload_id': upload_id,
        'source_type': 3,
        'poster_frame_index': 0,
        'length': 0.00,
        'audio_muted': False,
        'filter_type': 0,
        'video_result': 'deprecated',
        'clips': {
            'length': clipInfo['duration'],
            'source_type': '3',
            'camera_position': 'back',
        },
        'extra': {
            'source_width': clipInfo['width'],
            'source_height': clipInfo['height'],
        },
        'device': self.device_settings,
        'caption': caption,
    })
    return self.send_request('media/configure/?video=1', data)


def resize_video(self, fname):
    from os import rename
    self.logger.info("VID - \033[1;32mVIDEO: %s\033[0m" % fname)
    thumbnail = create_thumbnail(fname)
    if not thumbnail:
        self.logger.error("Error creating thumbnail...")
        return False
    ext = fname.split('.')[-1]
    name = fname.strip(".%s" % ext)
    self.logger.info("VID - finding video info...")
    try:
        res = Popen(["ffprobe",
                     "-v", "error",
                     "-select_streams", "v:0",
                     "-show_entries", "stream=height,width",
                     "-sexagesimal",
                     "-show_entries", "stream_tags=rotate",
                     "-of", "csv=s=x:p=0",
                     "%s" % fname], stdout=PIPE)
        res_array = res.stdout.read().strip().split('x')
        width = int(res_array[0])
        height = int(res_array[1])
        if len(res_array) > 2:
            rotation = int(res_array[2])
        else:
            rotation = 0
    except Exception as e:
        self.logger.error("VID - \033[41mERROR: %s\033[0m" % e)
        return False
    if rotation == 90 or rotation == 270:
        self.logger.info("VID - Rotated video")
        width, height = height, width
    self.logger.info("VID - FOUND w:%s h:%s (r:%s)" % (width, height, rotation))
    ratio = (width * 1.0) / (height * 1.0)
    rename(fname, "%s.ORIGINAL.%s" % (name, ext))
    # HORIZONTAL
    if width > height:
        self.logger.info("VID - HORIZONTAL VIDEO")
        if ratio > (16. / 9.):
            self.logger.info("VID - CROPPING...")
            vf = "scale=-1:450, crop=800:450"
        else:
            vf = "scale=800:-1"
    # VERTICAL
    elif width < height:
        self.logger.info("VID - VERTICAL")
        if ratio < (4. / 5.):
            self.logger.info("VID - CROPPING")
            vf = "scale=-1:800, crop=640:800"
        else:
            vf = "scale=-1:800"
    # SQUARE
    else:
        self.logger.info("VID - SQUARE")
        vf = "scale=800:800"
    self.logger.info("VID - FFMPEG... with `-vf {}`".format(vf))
    res = Popen(["ffmpeg",
                 "-i", "%s.ORIGINAL.%s" % (name, ext),
                 "-ss", "0",
                 "-t", "20",
                 "-vf", vf,
                 fname], stdout=PIPE)
    self.logger.info("VID - FFMPEG OK")
    self.logger.info("VID - CREATING THUMBNAIL...")
    thumbnail = create_thumbnail(fname)
    if not thumbnail:
        self.logger.error("Error creating thumbnail...")
        return False
    self.logger.info("VID - THUMBNAIL OK")
    rename("%s.ORIGINAL.%s" % (name, ext), "%s.ORIGINAL.%s.REMOVE_ME" % (name, ext))
    return thumbnail


def create_thumbnail(fname):
    thumbnail = "%s.thumbnail.jpg" % fname
    try:
        Popen(["convert",
               "%s[0]" % fname,
               thumbnail], stdout=PIPE)
    except Exception as e:
        print("VID - \033[41mERROR: %s\033[0m" % e)
        return False
    return thumbnail
