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
    broken_items = []
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
        if not self.follow(user_id):
            if self.api.last_response.status_code == 404:
                self.console_print("404 error user {user_id} doesn't exist.", 'red')
                broken_items.append(user_id)

            elif self.api.last_response.status_code == 200:
                broken_items.append(user_id)

            elif self.api.last_response.status_code not in (400, 429):
                # 400 (block to follow) and 429 (many request error)
                # which is like the 500 error.
                try_number = 3
                error_pass = False
                for _ in range(try_number):
                    time.sleep(60)
                    error_pass = self.follow(user_id)
                    if error_pass:
                        break
                if not error_pass:
                    self.error_delay()
                    i = user_ids.index(user_id)
                    broken_items += user_ids[i:]
                    break

    self.logger.info("DONE: Now following {} users in total.".format(self.total['follows']))
    return broken_items


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


def approve_pending_follow_requests(self):
    pending = self.get_pending_follow_requests()
    if pending:
        for u in tqdm(pending, desc='Approving users'):
            user_id = u["pk"]
            username = u["username"]
            self.api.approve_pending_friendship(user_id)
            if self.api.last_response.status_code != 200:
                self.logger.error("Could not approve {}".format(username))
        self.logger.info("DONE: {} people approved.".format(len(pending)))
        return True


def reject_pending_follow_requests(self):
    pending = self.get_pending_follow_requests()
    if pending:
        for u in tqdm(pending, desc='Rejecting users'):
            user_id = u["pk"]
            username = u["username"]
            self.api.reject_pending_friendship(user_id)
            if self.api.last_response.status_code != 200:
                self.logger.error("Could not approve {}".format(username))
        self.logger.info("DONE: {} people rejected.".format(len(pending)))
        return True
