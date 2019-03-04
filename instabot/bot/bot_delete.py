from tqdm import tqdm


def delete_media(self, media_id):
    self.small_delay()
    media = self.get_media_info(media_id)
    media = media[0] if isinstance(media, list) else media
    if self.api.delete_media(media):
        return True
    self.logger.info("Media with %s is not %s." % (media.get('id'), 'deleted'))
    return False


def delete_medias(self, medias):
    inx = 0
    if not medias:
        self.logger.info("Nothing to delete.")
        return False
    self.logger.info("Going to delete %d medias." % (len(medias)))
    for media in tqdm(medias):
        try:
            self.delete_media(media)
        except Exception as e:
            self.logger.error(str(e))
            inx += 1
            self.error_delay()
    self.logger.info("DONE: Total deleted %d medias." % (len(medias) - inx))
    return


def delete_comment(self, media_id, comment_id):
    if self.api.delete_comment(media_id, comment_id):
        self.small_delay()
        return True
    self.logger.info("Comment with %s in media %s is not deleted." % (comment_id, media_id))
    return False
