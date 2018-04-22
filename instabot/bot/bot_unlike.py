from tqdm import tqdm


def unlike(self, media_id):
    if not self.reached_limit('unlikes'):
        self.delay('unlike')
        if self.api.unlike(media_id):
            self.total['unlikes'] += 1
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
    self.logger.info("DONE: Total unliked %d medias." % self.total['unlikes'])
    return broken_items


def unlike_user(self, user_id):
    self.logger.info("Going to unlike user %s's feed:" % user_id)
    user_id = self.convert_to_user_id(user_id)
    medias = self.get_user_medias(user_id, filtration=False)
    return self.unlike_medias(medias)
