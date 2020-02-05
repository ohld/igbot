from tqdm import tqdm


def unlike(self, media_id):
    if not self.reached_limit("unlikes"):
        self.delay("unlike")
        if self.api.unlike(media_id):
            self.total["unlikes"] += 1
            return True
    else:
        self.logger.info("Out of unlikes for today.")
    return False


def unlike_comment(self, comment_id):
    if self.api.unlike_comment(comment_id):
        return True
    return False


def unlike_media_comments(self, media_id):
    broken_items = []
    media_comments = self.get_media_comments(media_id)
    comment_ids = [item["pk"] for item in media_comments if item["has_liked_comment"]]

    if not comment_ids:
        self.logger.info(
            "None comments received: comments not found"
            " or comments have been filtered."
        )
        return broken_items

    self.logger.info("Going to unlike %d comments." % (len(comment_ids)))

    for comment in tqdm(comment_ids):
        if not self.unlike_comment(comment):
            self.error_delay()
            broken_items = comment_ids[comment_ids.index(comment) :]
    self.logger.info(
        "DONE: Unliked {count} comments.".format(
            count=len(comment_ids) - len(broken_items)
        )
    )
    return broken_items


def unlike_medias(self, medias):
    broken_items = []
    self.logger.info("Going to unlike %d medias." % (len(medias)))
    for media in tqdm(medias):
        if not self.unlike(media):
            self.error_delay()
            broken_items = medias[medias.index(media) :]
            break
    self.logger.info("DONE: Total unliked %d medias." % self.total["unlikes"])
    return broken_items


def unlike_user(self, user_id):
    self.logger.info("Going to unlike user %s's feed:" % user_id)
    user_id = self.convert_to_user_id(user_id)
    medias = self.get_user_medias(user_id, filtration=False)
    return self.unlike_medias(medias)
