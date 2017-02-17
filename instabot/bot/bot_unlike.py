def unlike(self, media_id):
    if not self.check_media(media_id):
        return False
    if super(self.__class__, self).unlike(media_id):
        self.total_unliked += 1
        return True
    return False

def unlike_medias(self, media_ids):
    # TODO: unlike each media from list
    pass
