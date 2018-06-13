from tqdm import tqdm


def like(self, media_id):
    if not self.reached_limit('likes'):
        self.delay('like')
        if self.api.like(media_id):
            self.total['likes'] += 1
            return True
    else:
        self.logger.info("Out of likes for today.")
    return False


def like_comment(self, comment_id):
    if self.api.like_comment(comment_id):
        return True
    return False


def like_media_comments(self, media_id):
    broken_items = []
    media_comments = self.get_media_comments(media_id)
    comment_ids = [item["pk"] for item in media_comments if not item["has_liked_comment"]]

    if not comment_ids:
        self.logger.info("None comments received: comments not found or comments have been filtered.")
        return broken_items

    self.logger.info("Going to like %d comments." % (len(comment_ids)))

    for comment in tqdm(comment_ids):
        if not self.like_comment(comment):
            self.error_delay()
            broken_items = comment_ids[comment_ids.index(comment):]
    self.logger.info("DONE: Liked {count} comments.".format(
        count=len(comment_ids) - len(broken_items)
    ))
    return broken_items


def like_medias(self, medias):
    broken_items = []
    if not medias:
        self.logger.info("Nothing to like.")
        return broken_items
    self.logger.info("Going to like %d medias." % (len(medias)))
    for media in tqdm(medias):
        if not self.like(media):
            self.error_delay()
            broken_items = medias[medias.index(media):]
            break
    self.logger.info("DONE: Total liked %d medias." % self.total['likes'])
    return broken_items


def like_timeline(self, amount=None):
    self.logger.info("Liking timeline feed:")
    medias = self.get_timeline_medias()[:amount]
    return self.like_medias(medias)


def like_user(self, user_id, amount=None, filtration=True):
    """ Likes last user_id's medias """
    if filtration:
        if not self.check_user(user_id, filter_closed_acc=True):
            return False
    self.logger.info("Liking user_%s's feed:" % user_id)
    user_id = self.convert_to_user_id(user_id)
    medias = self.get_user_medias(user_id, filtration=filtration)
    if not medias:
        self.logger.info(
            "None medias received: account is closed or medias have been filtered.")
        return False
    return self.like_medias(medias[:amount])


def like_users(self, user_ids, nlikes=None, filtration=True):
    for user_id in user_ids:
        if self.reached_limit('likes'):
            self.logger.info("Out of likes for today.")
            return
        self.like_user(user_id, amount=nlikes, filtration=filtration)


def like_hashtag(self, hashtag, amount=None):
    """ Likes last medias from hashtag """
    self.logger.info("Going to like media with hashtag #%s." % hashtag)
    medias = self.get_total_hashtag_medias(hashtag, amount)
    return self.like_medias(medias)


def like_geotag(self, geotag, amount=None):
    # TODO: like medias by geotag
    pass


def like_followers(self, user_id, nlikes=None, nfollows=None):
    self.logger.info("Like followers of: %s." % user_id)
    if self.reached_limit('likes'):
        self.logger.info("Out of likes for today.")
        return
    if not user_id:
        self.logger.info("User not found.")
        return
    follower_ids = self.get_user_followers(user_id, nfollows)
    if not follower_ids:
        self.logger.info("%s not found / closed / has no followers." % user_id)
    else:
        self.like_users(follower_ids[:nfollows], nlikes)


def like_following(self, user_id, nlikes=None):
    self.logger.info("Like following of: %s." % user_id)
    if self.reached_limit('likes'):
        self.logger.info("Out of likes for today.")
        return
    if not user_id:
        self.logger.info("User not found.")
        return
    following_ids = self.get_user_following(user_id)
    if not following_ids:
        self.logger.info("%s not found / closed / has no following." % user_id)
    else:
        self.like_users(following_ids, nlikes)
