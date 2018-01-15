from tqdm import tqdm

from . import delay


def archive(self, media_id, undo=False):
    delay.small_delay(self)
    media = self.get_media_info(media_id)
    media = media[0] if isinstance(media, list) else media
    if super(self.__class__, self).archiveMedia(media, undo):
        self.total_archived += int(not undo)
        self.total_unarchived += int(undo)
        return True
    self.logger.info("Media with %s is not %s ." % media_id, 'unarchived' if undo else 'archived')
    return False


def archive_medias(self, medias):
    broken_items = []
    if not medias:
        self.logger.info("Nothing to archive.")
        return broken_items
    self.logger.info("Going to archive %d medias." % (len(medias)))
    for media in tqdm(medias):
        if not self.archive(media):
            delay.error_delay(self)
            broken_items = medias[medias.index(media):]
            break
    self.logger.info("DONE: Total archived %d medias." % self.total_archived)
    return broken_items


def unarchive_medias(self, medias):
    broken_items = []
    if not medias:
        self.logger.info("Nothing to unarchive.")
        return broken_items
    self.logger.info("Going to unarchive %d medias." % (len(medias)))
    for media in tqdm(medias):
        if not self.unarchive(media):
            delay.error_delay(self)
            broken_items = medias[medias.index(media):]
            break
    self.logger.info("DONE: Total unarchived %d medias." % self.total_unarchived)
    return broken_items
