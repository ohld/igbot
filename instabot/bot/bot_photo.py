import os
from io import open

from tqdm import tqdm

from . import delay


def upload_photo(self, photo, caption=None, upload_id=None):
    delay.small_delay(self)
    if super(self.__class__, self).uploadPhoto(photo, caption, upload_id):
        self.logger.info("Photo '%s' is %s ." % (photo, 'uploaded'))
        return True
    self.logger.info("Photo '%s' is not %s ." % (photo, 'uploaded'))
    return False


def download_photo(self, media_id, path='photos/', filename=None, description=False):
    delay.small_delay(self)
    if not os.path.exists(path):
        os.makedirs(path)
    if description:
        media = self.get_media_info(media_id)[0]
        caption = media['caption']['text']
        with open('{path}{0}_{1}.txt'.format(media['user']['username'], media_id, path=path), encoding='utf8', mode='w') as file_descriptor:
            file_descriptor.write(caption)
    try:
        photo = super(self.__class__, self).downloadPhoto(media_id, filename, False, path)
    except Exception:
        photo = False

    if photo:
        return photo
    self.logger.info("Media with %s is not %s ." % (media_id, 'downloaded'))
    return False


def download_photos(self, medias, path, description=False):
    broken_items = []
    if not medias:
        self.logger.info("Nothing to downloads.")
        return broken_items
    self.logger.info("Going to download %d medias." % (len(medias)))
    for media in tqdm(medias):
        if not self.download_photo(media, path, description=description):
            delay.error_delay(self)
            broken_items = medias[medias.index(media):]
            break
    return broken_items
