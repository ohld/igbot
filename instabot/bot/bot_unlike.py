from tqdm import tqdm

from . import limits


def unlike(self, media_id):
    if limits.check_if_bot_can_unlike(self):
        self.delay('unlike')
        if self.api.unlike(media_id):
            self.total['unliked'] += 1
            return True
    else:
        self.logger.info("Out of unlikes for today.")
    return False


def unlike_medias(self, medias):
    broken_items = []
    self.logger.info("Going to unlike %d medias." % (len(medias)))
    for media in tqdm(medias):
        if not self.unlike(media):
            self.error_delay()
            broken_items = medias[medias.index(media):]
            break
    self.logger.info("DONE: Total unliked %d medias." % self.total['unliked'])
    return broken_items


def unlike_user(self, user_id):
    self.logger.info("Going to unlike user %s's feed:" % user_id)
    user_id = self.convert_to_user_id(user_id)
    medias = self.get_user_medias(user_id, filtration=False)
    return self.unlike_medias(medias)
