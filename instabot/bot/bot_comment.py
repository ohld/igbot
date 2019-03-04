"""
    Bot functions to generate and post a comments.

    Instructions to file with comments:
        one line - one comment.

    Example:
        lol
        kek

"""
from tqdm import tqdm


def comment(self, media_id, comment_text):
    if self.is_commented(media_id):
        return True
    if not self.reached_limit('comments'):
        if self.blocked_actions['comments']:
            self.logger.warning('YOUR `COMMENT` ACTION IS BLOCKED')
            if self.blocked_actions_protection:
                from datetime import timedelta
                next_reset = (self.start_time.date() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
                self.logger.warning('blocked_actions_protection ACTIVE. Skipping `comment` action till, at least, {}.'.format(next_reset))
                return False
        self.delay('comment')
        _r = self.api.comment(media_id, comment_text)
        if _r == 'feedback_required':
            self.logger.error("`Comment` action has been BLOCKED...!!!")
            return False
        if _r:
            self.total['comments'] += 1
            return True
    else:
        self.logger.info("Out of comments for today.")
    return False


def reply_to_comment(self, media_id, comment_text, parent_comment_id):
    if not self.is_commented(media_id):
        self.logger.info("Media is not commented yet, nothing to answer to...")
        return False
    if not self.reached_limit('comments'):
        if self.blocked_actions['comments']:
            self.logger.warning('YOUR `COMMENT` ACTION IS BLOCKED')
            if self.blocked_actions_protection:
                self.logger.warning('blocked_actions_protection ACTIVE. Skipping `comment` action.')
                return False
        self.delay('comment')
        if comment_text[0] != '@':
            self.logger.error("A reply must start with mention, so '@' must be the 1st char, followed by the username you're replying to")
            return False
        if comment_text.split(' ')[0][1:] == self.get_username_from_user_id(self.user_id):
            self.logger.error("You can't reply to yourself")
            return False
        _r = self.api.reply_to_comment(media_id, comment_text, parent_comment_id)
        if _r == 'feedback_required':
            self.logger.error("`Comment` action has been BLOCKED...!!!")
            return False
        if _r:
            self.logger.info('Replied to comment {} of media {}'.format(parent_comment_id, media_id))
            self.total['comments'] += 1
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
                self.delay('comment')
                broken_items = medias[medias.index(media):]
                break
    self.logger.info("DONE: Total commented on %d medias. " %
                     self.total['comments'])
    return broken_items


def comment_hashtag(self, hashtag, amount=None):
    self.logger.info("Going to comment medias by %s hashtag" % hashtag)
    medias = self.get_total_hashtag_medias(hashtag, amount)
    return self.comment_medias(medias)


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
        if self.reached_limit('comments'):
            self.logger.info("Out of comments for today.")
            return
        self.comment_user(user_id, amount=ncomments)


def comment_geotag(self, geotag):
    # TODO: comment every media from geotag
    pass


def is_commented(self, media_id):
    return self.user_id in self.get_media_commenters(media_id)
