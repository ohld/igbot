from tqdm import tqdm

from . import delay


def unlike(self, media_id):
    if super(self.__class__, self).unlike(media_id):
        self.total_unliked += 1
        return True
    return False


def unlike_medias(self, medias):
    broken_items = []
    self.logger.info("Going to unlike %d medias." % (len(medias)))
    for media in tqdm(medias):
        if not self.unlike(media):
            delay.error_delay(self)
            broken_items.append(media)
    self.logger.info("DONE: Total liked %d medias." % self.total_liked)
    return broken_items
