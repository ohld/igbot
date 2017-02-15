import time
import random
from tqdm import tqdm

def like(self, media_id):
    if not self.check_media(media_id):
        return False
    if super(self.__class__, self).like(media_id):
        self.total_liked += 1
        return True
    return False

def like_medias(self, medias):
    """ medias - list of ["pk"] fields of response """
    self.logger.info("    Going to like %d medias." % (len(medias)))
    total_liked = 0
    for media in tqdm(medias):
        if self.like(media):
            total_liked += 1
        else:
            pass
        time.sleep(10 * random.random())
    self.logger.info("    DONE: Total liked %d medias. " % total_liked)
    return True

def like_timeline(self, amount=None):
    """ Likes last 8 medias from timeline feed """
    self.logger.info("Liking timeline feed:")
    medias = self.get_timeline_medias()[:amount]
    return self.like_medias(medias)

def like_user_id(self, user_id, amount=None):
    """ Likes last user_id's medias """
    if not user_id:
        return False
    self.logger.info("Liking user_%s's feed:" % user_id)
    medias = self.get_user_medias(user_id)
    if not medias:
        self.logger.info("  Can't like user: account is closed!")
        return False
    return self.like_medias(medias[:amount])

def like_hashtag(self, hashtag, amount=None):
    """ Likes last medias from hashtag """
    self.logger.info("Going to like media with hashtag #%s" % hashtag)
    medias = self.get_hashtag_medias(hashtag)
    return self.like_medias(medias[:amount])

def like_geotag(self, geotag, amount=None):
    # TODO: like medias by geotag
    pass
