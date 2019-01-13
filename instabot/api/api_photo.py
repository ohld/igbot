import imghdr
import os
import shutil
import struct
import time

from requests_toolbelt import MultipartEncoder

from . import config


def download_photo(self, media_id, filename, media=False, folder='photos'):
    if not media:
        self.media_info(media_id)
        if not self.last_json.get('items'):
            return True
        media = self.last_json['items'][0]
    if media['media_type'] == 2:
        return True
    elif media['media_type'] == 1:
        filename = ('{}_{}.jpg'.format(media['user']['username'], media_id)
                    if not filename else '{}.jpg'.format(filename))
        images = media['image_versions2']['candidates']
        fname = os.path.join(folder, filename)
        if os.path.exists(fname):
            return os.path.abspath(fname)
        response = self.session.get(images[0]['url'], stream=True)
        if response.status_code == 200:
            with open(fname, 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
            return os.path.abspath(fname)
    else:
        success = False
        video_included = False
        for index in range(len(media["carousel_media"])):
            if media["carousel_media"][index]["media_type"] != 1:
                video_included = True
                continue
            filename_i = ('{}_{}_{}.jpg'.format(media['user']['username'], media_id, index)
                          if not filename else '{}_{}.jpg'.format(filename, index))
            images = media["carousel_media"][index]["image_versions2"]["candidates"]
            fname = os.path.join(folder, filename_i)
            if os.path.exists(fname):
                return os.path.abspath(fname)
            response = self.session.get(images[0]['url'], stream=True)
            if response.status_code == 200:
                success = True
                with open(fname, 'wb') as f:
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, f)
        if success:
            return os.path.abspath(fname)
        elif video_included:
            return True


def compatible_aspect_ratio(size):
    min_ratio, max_ratio = 4.0 / 5.0, 90.0 / 47.0
    width, height = size
    ratio = width / height
    return min_ratio <= ratio <= max_ratio


def configure_photo(self, upload_id, photo, caption=''):
    (w, h) = get_exiftool_image_size(photo)
    data = self.json_data({
        'media_folder': 'Instagram',
        'source_type': 4,
        'caption': caption,
        'upload_id': upload_id,
        'device': self.device_settings,
        'edits': {
            'crop_original_size': [w * 1.0, h * 1.0],
            'crop_center': [0.0, 0.0],
            'crop_zoom': 1.0
        },
        'extra': {
            'source_width': w,
            'source_height': h,
        }})
    return self.send_request('media/configure/?', data)


def upload_photo(self, photo, caption=None, upload_id=None):
    if upload_id is None:
        upload_id = str(int(time.time() * 1000))
    resized_photo = resize_picture(photo)
    if not resized_photo:
        self.logger.error("Error resizing photo. Aborting upload.")
        return False
    data = {
        'upload_id': upload_id,
        '_uuid': self.uuid,
        '_csrftoken': self.token,
        'image_compression': '{"lib_name":"jt","lib_version":"1.3.0","quality":"87"}',
        'photo': ('pending_media_%s.jpg' % upload_id, open(photo, 'rb'), 'application/octet-stream', {'Content-Transfer-Encoding': 'binary'})
    }
    m = MultipartEncoder(data, boundary=self.uuid)
    self.session.headers.update({'X-IG-Capabilities': '3Q4=',
                                 'X-IG-Connection-Type': 'WIFI',
                                 'Cookie2': '$Version=1',
                                 'Accept-Language': 'en-US',
                                 'Accept-Encoding': 'gzip, deflate',
                                 'Content-type': m.content_type,
                                 'Connection': 'close',
                                 'User-Agent': self.user_agent})
    response = self.session.post(
        config.API_URL + "upload/photo/", data=m.to_string())
    if response.status_code == 200:
        if self.configure_photo(upload_id, photo, caption):
            self.expose()
            return True
    return False


def get_image_size(fname):
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


def resize_picture(fname):
    from subprocess import Popen, PIPE
    from os import rename, remove
    from distutils.spawn import find_executable
    requirements = ['exiftool', 'convert']
    for requirement in requirements:
        if find_executable(requirement) is None:
            print("{} not found in your OS. Please install and retry".format(requirement))
            return False
        if requirement == 'convert':
            res = Popen(['convert', '--version'], stdout=PIPE)
            inf = res.stdout.read()
            ver = inf.split(' ')[2]
            if ver[0] != '7':
                print("WARNING: your `convert` version is `{}`\n."
                      "Version 7.x is required to crop images.\n"
                      "This could cause errors. Consider upgrading.\n"
                      "Hit ctrl-C within 20 seconds to abort...".format(ver))
                from time import sleep
                sleep(20)
    default = 1080
    ext = fname.split('.')[-1]
    name = fname.strip(".%s" % ext)
    try:
        pic_info = {}
        res = Popen(["identify", "-format", "%w", fname], stdout=PIPE)
        pic_info['width'] = int( res.stdout.read())
        res = Popen(["identify", "-format", "%h", fname], stdout=PIPE)
        pic_info['height'] = int( res.stdout.read())
        try:
            res = Popen(["identify", "-format" , "%[EXIF:Orientation]", fname], stdout=PIPE)
            pic_info['rotation'] = int( res.stdout.read())
        except:
            pic_info['rotation'] = 0
    except Exception as e:
        print("ERROR: {}".format(e))
        return False
    width, height = pic_info['width'], pic_info['height']
    degrees = "0"
    if 'rotation' in pic_info:
        if pic_info['rotation'] == 8:
            width, height = height, width
            degrees = "270"
        elif pic_info['rotation'] == 6:
            width, height = height, width
            degrees = "90"
        elif pic_info['rotation'] == 3:
            degrees = "180"
        print("Rotated picture deg: {}".format(degrees))
    print("FOUND width:{} height:{}".format(width, height))
    ratio = (width * 1.) / (height * 1.)
    if width > height and ratio > (90. / 47.):
        print("Resize and crop horizontal picture...")
        res = Popen(["convert",
                     fname,
                     "-gravity" , "center",
                     "-crop", "90:47",
                     "-resize", "{default}x{default}".format(default=default),
                     "-rotate", degrees,
                     "{}.TMP.jpg".format(name)], stdout=PIPE)
        out = res.stdout.read()
        print(out)
    elif width < height and ratio < (4. / 5.):
        print("Resize and crop vertical picture...")
        res = Popen(["convert",
                     fname,
                     "-gravity" , "center",
                     "-crop", "5:4",
                     "-resize", "{default}x{default}".format(default=default),
                     "-rotate", degrees,
                     "{}.TMP.jpg".format(name)], stdout=PIPE)
        out = res.stdout.read()
        print(out)
    else:
        print("Resize picture...")
        res = Popen(["convert",
                     fname,
                     "-gravity" , "center",
                     "-resize", "{default}x{default}".format(default=default),
                     "-rotate", degrees,
                     "{}.TMP.jpg".format(name)], stdout=PIPE)
        out = res.stdout.read()
        print(out)
    print("Strip exif metadata...")
    res = Popen(["exiftool",
                 "-all=",
                 "{}.TMP.jpg".format(name)], stdout=PIPE)
    out = res.stdout.read()
    print(out)
    print("DONE :-)")
    rename(fname, "{}.ORIGINAL".format(fname))
    rename("{}.TMP.jpg".format(name), "{}.jpg".format(name))
    return "{}.jpg".format(name)


def get_exiftool_image_size(fname):
    print("Getting image size...")
    import re
    from subprocess import Popen, PIPE, STDOUT
    exif_info = {}
    try:
        xRes = Popen(["exiftool", fname], stdout=PIPE, stderr=STDOUT)
        for x in xRes.stdout.readlines():
            m = re.search(r'^image size.*:\s(\d+)x(\d+).*$', str(x), flags=re.IGNORECASE)
            if m is not None:
                exif_info['width'] = int(m.group(1))
                exif_info['height'] = int(m.group(2))
                print "width:'{}' height:'{}'".format(exif_info['width'], exif_info['height'])
    finally:
        if 'width' not in exif_info:
            print("ERROR getting image size with `exiftool`")
            return False, False
    return exif_info['width'], exif_info['height']
