from tqdm import tqdm

from . import delay


def download_photo(self, media_id, path='photos/', filename=None):
    delay.small_delay(self)
    photo = super(self.__class__, self).downloadPhoto(media_id, filename, False, path)
    if photo:
        return photo
    self.logger.info("Media with %s is not %s ." % media_id, 'downloaded')
    return False


def download_photos(self, medias, path):
    broken_items = []
    if len(medias) == 0:
        self.logger.info("Nothing to downloads.")
        return broken_items
    self.logger.info("Going to download %d medias." % (len(medias)))
    for media in tqdm(medias):
        if not self.download(media, path):
            delay.error_delay(self)
            broken_items = medias[medias.index(media):]
            break
    return broken_items
