from tqdm import tqdm

from . import delay


def delete_media(self, media_id):
    delay.small_delay(self)
    media = self.get_media_info(media_id)
    media = media[0] if isinstance(media, list) else media
    if super(self.__class__, self).deleteMedia(media):
        return True
    self.logger.info("Media with %s is not %s." % (media.get('id'), 'deleted'))
    return False


def delete_medias(self, medias):
    broken_items = []
    if not medias:
        self.logger.info("Nothing to delete.")
        return broken_items
    self.logger.info("Going to delete %d medias." % (len(medias)))
    for media in tqdm(medias):
        if not self.delete_media(media):
            delay.error_delay(self)
            broken_items = medias[medias.index(media):]
            break
    self.logger.info("DONE: Total deleted %d medias." % (len(medias) - len(broken_items)))
    return broken_items


def delete_comment(self, media_id, comment_id):
    if super(self.__class__, self).deleteComment(media_id, comment_id):
        delay.small_delay(self)
        return True
    self.logger.info("Comment with %s in media %s is not deleted." % (comment_id, media_id))
    return False
