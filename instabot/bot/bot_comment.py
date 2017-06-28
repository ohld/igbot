"""
    Bot functions to generate and post a comments.

    Instructions to file with comments:
        one line - one comment.

    Example:
        lol
        kek

"""
from tqdm import tqdm

from . import limits, delay


def comment(self, media_id, comment_text):
    if self.is_commented(media_id):
        return True
    if limits.check_if_bot_can_comment(self):
        delay.comment_delay(self)
        if super(self.__class__, self).comment(media_id, comment_text):
            self.total_commented += 1
            return True
    else:
        self.logger.info("Out of comments for today.")
    return False


def comment_medias(self, medias):
    broken_items = []
    self.logger.info("Going to comment %d medias." % (len(medias)))
    for media in tqdm(medias):
        if not self.is_commented(media):
            text = self.get_comment()
            self.logger.info("Commented with text: %s" % text)
            if not self.comment(media, text):
                delay.comment_delay(self)
                broken_items = medias[medias.index(media):]
                break
    self.logger.info("DONE: Total commented on %d medias. " %
                     self.total_commented)
    return broken_items


def comment_hashtag(self, hashtag, amount=None):
    self.logger.info("Going to comment medias by %s hashtag" % hashtag)
    medias = self.get_hashtag_medias(hashtag)
    return self.comment_medias(medias[:amount])


def comment_user(self, user_id, amount=None):
    """ Comments last user_id's medias """
    if not self.check_user(user_id, filter_closed_acc=True):
        return False
    self.logger.info("Going to comment user_%s's feed:" % user_id)
    user_id = self.convert_to_user_id(user_id)
    medias = self.get_user_medias(user_id, is_comment=True)
    if not medias:
        self.logger.info(
            "None medias received: account is closed or medias have been filtered.")
        return False
    return self.comment_medias(medias[:amount])


def comment_users(self, user_ids, ncomments=None):
    for user_id in user_ids:
        if not limits.check_if_bot_can_comment(self):
            self.logger.info("Out of comments for today.")
            return
        self.comment_user(user_id, amount=ncomments)


def comment_geotag(self, geotag):
    # TODO: comment every media from geotag
    pass


def is_commented(self, media_id):
    return self.user_id in self.get_media_commenters(media_id)
