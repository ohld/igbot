from tqdm import tqdm

from . import limits
from . import delay


def unlike(self, media_id):
    if limits.check_if_bot_can_unlike(self):
        delay.like_delay(self)
        if super(self.__class__, self).unlike(media_id):
            self.total_unliked += 1
            return True
    else:
        self.logger.info("Out of unlikes for today.")
    return False


def unlike_medias(self, medias):
    broken_items = []
    self.logger.info("Going to unlike %d medias." % (len(medias)))
    for media in tqdm(medias):
        if not self.unlike(media):
            delay.error_delay(self)
            broken_items.append(media)
    self.logger.info("DONE: Total unliked %d medias." % self.total_unliked)
    return broken_items
