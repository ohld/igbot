"""
    Bot functions to generate and post a comments.

    Instructions to file with comments:
        one line - one comment.

    Example:
        lol
        kek

"""
import time
import random
import os
import io
from tqdm import tqdm

def comment(self, media_id, comment_text):
    if not self.check_media(media_id):
        return False
    if super(self.__class__, self).comment(media_id, comment_text):
        self.total_commented += 1
        return True
    return False

def comment_medias(self, medias):
    """ medias - list of ["pk"] fields of response """
    self.logger.info("Going to comment on %d medias." % (len(medias)))
    for media in tqdm(medias):
        if not self.is_commented(media):
            self.comment(media, self.get_comment())
            time.sleep(30 * random.random() + 30)
    self.logger.info("DONE: Total commented on %d medias. " % self.total_commented)
    return True

def comment_hashtag(self, hashtag, amount=None):
    self.logger.info("Going to comment medias by %s hashtag" % hashtag)
    medias = self.get_hashtag_medias(hashtag)
    return self.comment_medias(medias[:amount])

def comment_users(self, user_ids):
    # TODO: Put a comment to last media of every user from list
    pass

def comment_geotag(self, geotag):
    # TODO: comment every media from geotag
    pass

def is_commented(self, media_id):
    # TODO: get_media_commenters returns _usernames_ not user_ids!
    # TODO: implement self.user_id and change the method
    return self.username in self.get_media_commenters(media_id)
