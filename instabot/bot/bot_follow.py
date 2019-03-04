import time

from tqdm import tqdm


def follow(self, user_id):
    user_id = self.convert_to_user_id(user_id)
    msg = ' ===> Going to follow `user_id`: {}.'.format(user_id)
    self.console_print(msg)
    if not self.check_user(user_id):
        return False
    if not self.reached_limit('follows'):
        self.delay('follow')
        if self.api.follow(user_id):
            msg = '===> FOLLOWED <==== `user_id`: {}.'.format(user_id)
            self.console_print(msg, 'green')
            self.total['follows'] += 1
            self.followed_file.append(user_id)
            if user_id not in self.following:
                self.following.append(user_id)
            return True
    else:
        self.logger.info("Out of follows for today.")
    return False


def follow_users(self, user_ids):
    if self.reached_limit('follows'):
        self.logger.info("Out of follows for today.")
        return
    msg = "Going to follow {} users.".format(len(user_ids))
    self.logger.info(msg)
    skipped = self.skipped_file
    followed = self.followed_file
    unfollowed = self.unfollowed_file
    self.console_print(msg, 'green')

    # Remove skipped and already followed and unfollowed list from user_ids
    user_ids = list(set(user_ids) - skipped.set - followed.set - unfollowed.set)
    msg = 'After filtering followed, unfollowed and `{}`, {} user_ids left to follow.'
    msg = msg.format(skipped.fname, len(user_ids))
    self.console_print(msg, 'green')
    for user_id in tqdm(user_ids, desc='Processed users'):
        if self.reached_limit('follows'):
            self.logger.info("Out of follows for today.")
            break
        try:
            self.follow(user_id)
        except Exception as e:
            self.logger.error(str(e))
            self.error_delay()

    self.logger.info("DONE: Now following {} users in total.".format(self.total['follows']))
    return


def follow_followers(self, user_id, nfollows=None):
    self.logger.info("Follow followers of: {}".format(user_id))
    if self.reached_limit('follows'):
        self.logger.info("Out of follows for today.")
        return
    if not user_id:
        self.logger.info("User not found.")
        return
    followers = self.get_user_followers(user_id, nfollows)
    followers = list(set(followers) - set(self.blacklist))
    if not followers:
        self.logger.info("{} not found / closed / has no followers.".format(user_id))
    else:
        self.follow_users(followers[:nfollows])


def follow_following(self, user_id, nfollows=None):
    self.logger.info("Follow following of: {}".format(user_id))
    if self.reached_limit('follows'):
        self.logger.info("Out of follows for today.")
        return
    if not user_id:
        self.logger.info("User not found.")
        return
    followings = self.get_user_following(user_id)
    if not followings:
        self.logger.info("{} not found / closed / has no following.".format(user_id))
    else:
        self.follow_users(followings[:nfollows])
