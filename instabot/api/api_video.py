import json
import time
import copy
import math

from moviepy.editor import VideoFileClip
from requests_toolbelt import MultipartEncoder

from . import config

def configureVideo(self, upload_id, video, thumbnail, caption = ''):
    clip = VideoFileClip(video)
    self.uploadPhoto(photo=thumbnail, caption=caption, upload_id=upload_id)
    data = json.dumps({
        'upload_id': upload_id,
        'source_type': 3,
        'poster_frame_index': 0,
        'length': 0.00,
        'audio_muted': False,
        'filter_type': 0,
        'video_result': 'deprecated',
        'clips': {
            'length': clip.duration,
            'source_type': '3',
            'camera_position': 'back',
        },
        'extra': {
            'source_width': clip.size[0],
            'source_height': clip.size[1],
        },
        'device': config.DEVICE_SETTINTS,
        '_csrftoken': self.token,
        '_uuid': self.uuid,
        '_uid': self.username_id,
        'caption': caption,
    })
    return self.SendRequest('media/configure/?video=1', self.generateSignature(data))

def uploadVideo(self, video, thumbnail, caption = None, upload_id = None):
    if upload_id is None:
        upload_id = str(int(time.time() * 1000))
    data = {
        'upload_id': upload_id,
        '_csrftoken': self.token,
        'media_type': '2',
        '_uuid': self.uuid,
    }
    m = MultipartEncoder(data, boundary=self.uuid)
    self.s.headers.update({'X-IG-Capabilities': '3Q4=',
                           'X-IG-Connection-Type': 'WIFI',
                           'Host': 'i.instagram.com',
                           'Cookie2': '$Version=1',
                           'Accept-Language': 'en-US',
                           'Accept-Encoding': 'gzip, deflate',
                           'Content-type': m.content_type,
                           'Connection': 'keep-alive',
                           'User-Agent': config.USER_AGENT})
    response = self.s.post(config.API_URL + "upload/video/", data=m.to_string())
    if response.status_code == 200:
        body = json.loads(response.text)
        upload_url = body['video_upload_urls'][3]['url']
        upload_job = body['video_upload_urls'][3]['job']

        videoData = open(video, 'rb').read()
        request_size = math.floor(len(videoData) / 4)
        lastRequestExtra = (len(videoData) - (request_size * 3))

        headers = copy.deepcopy(self.s.headers)
        self.s.headers.update({'X-IG-Capabilities': '3Q4=',
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
                               'User-Agent': config.USER_AGENT})
        for i in range(0, 4):
            start = i * request_size
            if i == 3:
                end = i * request_size + lastRequestExtra
            else:
                end = (i + 1) * request_size
            length = lastRequestExtra if i == 3 else request_size
            content_range = "bytes {start}-{end}/{lenVideo}".format(start=start, end=(end - 1),
                                                                    lenVideo=len(videoData)).encode('utf-8')

            self.s.headers.update({'Content-Length': str(end - start), 'Content-Range': content_range, })
            response = self.s.post(upload_url, data=videoData[start:start + length])
        self.s.headers = headers

        if response.status_code == 200:
            if self.configureVideo(upload_id, video, thumbnail, caption):
                self.expose()
    return False
