from tqdm import tqdm
import random
from . import limits
from . import delay


def like(self, media_id):
    if limits.check_if_bot_can_like(self):
        delay.like_delay(self)
        if super(self.__class__, self).like(media_id):
            self.total_liked += 1
            return True
    else:
        self.logger.info("Out of likes for today.")
    return False


def like_medias(self, medias):
    broken_items = []
    self.logger.info("Going to like %d medias." % (len(medias)))
    for media in tqdm(medias):
        if not self.like(media):
            delay.error_delay(self)
            broken_items.append(media)
    self.logger.info("DONE: Total liked %d medias." % self.total_liked)
    return broken_items


def like_timeline(self, amount=None):
    self.logger.info("Liking timeline feed:")
    medias = self.get_timeline_medias()[:amount]
    return self.like_medias(medias)


def like_user(self, user_id, amount=None):
    """ Likes last user_id's medias """
    if not self.check_user(user_id):
        return False
    self.logger.info("Liking user_%s's feed:" % user_id)
    user_id = self.convert_to_user_id(user_id)
    medias = self.get_user_medias(user_id)
    if not medias:
        self.logger.info(
            "None medias recieved: account is closed or medias have been filtered.")
        return False
    size = min(len(medias), amount)
    return self.like_medias(random.sample(medias, size))


def like_users(self, user_ids, nlikes=None):
    for user_id in user_ids:
        self.like_user(user_id, amount=nlikes)


def like_hashtag(self, hashtag, amount=None):
    """ Likes last medias from hashtag """
    self.logger.info("Going to like media with hashtag #%s." % hashtag)
    medias = self.get_hashtag_medias(hashtag)
    return self.like_medias(medias[:amount])


def like_geotag(self, geotag, amount=None):
    # TODO: like medias by geotag
    pass


def like_followers(self, user_id, nlikes=None):
    self.logger.info("Like followers of: %s." % user_id)
    if not user_id:
        self.logger.info("User not found.")
        return
    follower_ids = self.get_user_followers(user_id[0])
    if not follower_ids:
        self.logger.info("%s not found / closed / has no followers." % user_id)
    else:
        self.like_users(follower_ids, nlikes)


def like_following(self, user_id, nlikes=None):
    self.logger.info("Like following of: %s." % user_id)
    if not user_id:
        self.logger.info("User not found.")
        return
    following_ids = self.get_user_following(user_id[0])
    if not following_ids:
        self.logger.info("%s not found / closed / has no following." % user_id)
    else:
        self.like_users(following_ids, nlikes)
