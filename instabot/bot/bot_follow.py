from tqdm import tqdm

from . import delay, limits


def follow(self, user_id):
    user_id = self.convert_to_user_id(user_id)
    msg = ' ===> Going to follow `user_id`: {}.'.format(user_id)
    self.console_print(msg)
    if not self.check_user(user_id):
        return True
    if limits.check_if_bot_can_follow(self):
        delay.follow_delay(self)
        if self.api.follow(user_id):
            msg = '===> FOLLOWED <==== `user_id`: {}.'.format(user_id)
            self.console_print(msg, 'green')
            self.total_followed += 1
            self.followed_file.append(user_id)
            return True
    else:
        self.logger.info("Out of follows for today.")
    return False


def follow_users(self, user_ids):
    broken_items = []
    if not limits.check_if_bot_can_follow(self):
        self.logger.info("Out of follows for today.")
        return
    msg = "Going to follow {} users.".format(len(user_ids))
    self.logger.info(msg)
    followed = self.followed_file
    skipped = self.skipped_file
    self.console_print(msg, 'green')

    # Remove skipped and followed list from user_ids
    user_ids = list(set(user_ids) - followed.set - skipped.set)
    msg = 'After filtering `{}` and `{}`, {} user_ids left to follow.'
    msg = msg.format(followed.fname, skipped.fname, len(user_ids))
    self.console_print(msg, 'green')
    for user_id in tqdm(user_ids, desc='Processed users'):
        if not self.follow(user_id):
            if self.last_response.status_code == 404:
                self.console_print("404 error user {user_id} doesn't exist.", 'red')
                broken_items.append(user_id)

            elif self.last_response.status_code not in (400, 429):
                # 400 (block to follow) and 429 (many request error)
                # which is like the 500 error.
                try_number = 3
                error_pass = False
                for _ in range(try_number):
                    delay_time = 60
                    delay.delay_in_seconds(self, delay_time)
                    error_pass = self.follow(user_id)
                    if error_pass:
                        break
                if not error_pass:
                    delay.error_delay(self)
                    i = user_ids.index(user_id)
                    broken_items += user_ids[i:]
                    break

    self.logger.info("DONE: Followed {} users in total.".format(self.total_followed))
    return broken_items


def follow_followers(self, user_id, nfollows=None):
    self.logger.info("Follow followers of: {}".format(user_id))
    if not limits.check_if_bot_can_follow(self):
        self.logger.info("Out of follows for today.")
        return
    if not user_id:
        self.logger.info("User not found.")
        return
    followers = self.get_user_followers(user_id, nfollows)
    if not followers:
        self.logger.info("{} not found / closed / has no followers.".format(user_id))
    else:
        self.follow_users(followers[:nfollows])


def follow_following(self, user_id, nfollows=None):
    self.logger.info("Follow following of: {}".format(user_id))
    if not limits.check_if_bot_can_follow(self):
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
