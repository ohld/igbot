from tqdm import tqdm


def archive(self, media_id, undo=False):
    self.small_delay()
    media = self.get_media_info(media_id)
    media = media[0] if isinstance(media, list) else media
    if self.api.archive_media(media, undo):
        self.total['archived'] += int(not undo)
        self.total['unarchived'] += int(undo)
        return True
    self.logger.info("Media id %s is not %s.", media_id, 'unarchived' if undo else 'archived')
    return False


def archive_medias(self, medias):
    if not medias:
        self.logger.info("Nothing to archive.")
        return False
    self.logger.info("Going to archive %d medias." % (len(medias)))
    for media in tqdm(medias):
        try:
            self.archive(media)
        except Exception as e:
            self.logger.error(str(e))
            self.error_delay()
    self.logger.info("DONE: Total archived %d medias." % self.total['archived'])
    return


def unarchive_medias(self, medias):
    if not medias:
        self.logger.info("Nothing to unarchive.")
        return False
    self.logger.info("Going to unarchive %d medias." % (len(medias)))
    for media in tqdm(medias):
        try:
            self.unarchive(media)
        except Exception as e:
            self.logger.error(str(e))
            self.error_delay()
    self.logger.info("DONE: Total unarchived %d medias." % self.total['unarchived'])
    return 
