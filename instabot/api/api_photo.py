import struct
import imghdr
import time
import json
import shutil
import os

from requests_toolbelt import MultipartEncoder

from . import config


def downloadPhoto(self, media_id, filename, media=False, path='photos/'):
    if not media:
        self.mediaInfo(media_id)
        media = self.LastJson['items'][0]
    filename = '{0}_{1}.jpg'.format(media['user']['username'], media_id) if not filename else '{0}.jpg'.format(filename)
    images = media['image_versions2']['candidates']
    if os.path.exists(path + filename):
        return os.path.abspath(path + filename)
    response = self.session.get(images[0]['url'], stream=True)
    if response.status_code == 200:
        with open(path + filename, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)
        return os.path.abspath(path + filename)


def compatibleAspectRatio(size):
    min_ratio, max_ratio = 4.0 / 5.0, 90.0 / 47.0
    width, height = size
    this_ratio = 1.0 * width / height
    return min_ratio <= this_ratio <= max_ratio


def configurePhoto(self, upload_id, photo, caption=''):
    (w, h) = getImageSize(photo)
    data = json.dumps({
        '_csrftoken': self.token,
        'media_folder': 'Instagram',
        'source_type': 4,
        '_uid': self.user_id,
        '_uuid': self.uuid,
        'caption': caption,
        'upload_id': upload_id,
        'device': config.DEVICE_SETTINTS,
        'edits': {
            'crop_original_size': [w * 1.0, h * 1.0],
            'crop_center': [0.0, 0.0],
            'crop_zoom': 1.0
        },
        'extra': {
            'source_width': w,
            'source_height': h,
        }})
    return self.SendRequest('media/configure/?', self.generateSignature(data))


def uploadPhoto(self, photo, caption=None, upload_id=None):
    if upload_id is None:
        upload_id = str(int(time.time() * 1000))
    if not compatibleAspectRatio(getImageSize(photo)):
        self.logger.info('Not compatible photo aspect ratio')
        return False
    with open(photo, 'rb') as photo_bytes:
        data = {
            'upload_id': upload_id,
            '_uuid': self.uuid,
            '_csrftoken': self.token,
            'image_compression': '{"lib_name":"jt","lib_version":"1.3.0","quality":"87"}',
            'photo': ('pending_media_%s.jpg' % upload_id, photo_bytes, 'application/octet-stream', {'Content-Transfer-Encoding': 'binary'})
        }
    m = MultipartEncoder(data, boundary=self.uuid)
    self.session.headers.update({'X-IG-Capabilities': '3Q4=',
                                 'X-IG-Connection-Type': 'WIFI',
                                 'Cookie2': '$Version=1',
                                 'Accept-Language': 'en-US',
                                 'Accept-Encoding': 'gzip, deflate',
                                 'Content-type': m.content_type,
                                 'Connection': 'close',
                                 'User-Agent': config.USER_AGENT})
    response = self.session.post(
        config.API_URL + "upload/photo/", data=m.to_string())
    if response.status_code == 200:
        if self.configurePhoto(upload_id, photo, caption):
            self.expose()
            return True
    return False


def getImageSize(fname):
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            raise RuntimeError("Invalid Header")
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                raise RuntimeError("PNG: Invalid check")
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            fhandle.seek(0)  # Read 0xff next
            size = 2
            ftype = 0
            while not 0xc0 <= ftype <= 0xcf:
                fhandle.seek(size, 1)
                byte = fhandle.read(1)
                while ord(byte) == 0xff:
                    byte = fhandle.read(1)
                ftype = ord(byte)
                size = struct.unpack('>H', fhandle.read(2))[0] - 2
            # We are at a SOFn block
            fhandle.seek(1, 1)  # Skip `precision' byte.
            height, width = struct.unpack('>HH', fhandle.read(4))
        else:
            raise RuntimeError("Unsupported format")
        return width, height
