import os
from io import open

from tqdm import tqdm


def upload_photo(self, photo, caption=None, upload_id=None, from_video=False):
    self.small_delay()
    if self.api.upload_photo(photo, caption, upload_id, from_video):
        self.logger.info("Photo '{}' is uploaded.".format(photo))
        return True
    self.logger.info("Photo '{}' is not uploaded.".format(photo))
    return False


def download_photo(self, media_id, folder='photos', filename=None, save_description=False):
    self.small_delay()
    if not os.path.exists(folder):
        os.makedirs(folder)
    if save_description:
        media = self.get_media_info(media_id)[0]
        caption = media['caption']['text'] if media['caption'] else ''
        username = media['user']['username']
        fname = os.path.join(folder, '{}_{}.txt'.format(username, media_id))
        with open(fname, encoding='utf8', mode='w') as f:
            f.write(caption)
    try:
        return self.api.download_photo(media_id, filename, False, folder)
    except Exception:
        self.logger.info("Media with `{}` is not downloaded.".format(media_id))
        return False


def download_photos(self, medias, folder, save_description=False):
    broken_items = []
    if not medias:
        self.logger.info("Nothing to downloads.")
        return broken_items
    self.logger.info("Going to download {} medias.".format(len(medias)))
    for media in tqdm(medias):
        if not self.download_photo(media, folder, save_description=save_description):
            self.error_delay()
            broken_items = medias[medias.index(media):]
    return broken_items
