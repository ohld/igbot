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
        if super(self.__class__, self).follow(user_id):
            msg = '===> FOLLOWED <==== `user_id`: {}.'.format(user_id)
            self.console_print(msg, 'green')
            self.total_followed += 1
            self.console_print('Adding `user_id` to `followed.txt`.', 'green')
            with open('followed.txt', 'a') as f:
                f.write("{user_id}\n".format(user_id=user_id))
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
    followed = self.read_list_from_file("followed.txt")
    skipped = self.read_list_from_file("skipped.txt")
    self.console_print(msg, 'green')

    # Remove skipped and followed list from user_ids
    user_ids = list((set(user_ids) - set(followed)) - set(skipped))
    msg = 'After filtering `followed.txt` and `skipped.txt`, {} user_ids left to follow.'
    self.console_print(msg.format(len(user_ids)), 'green')
    for user_id in tqdm(user_ids, desc='Processed users'):
        if not self.follow(user_id):
            if self.last_response.status_code == 404:
                console_print("404 error user {user_id} doesn't exist.", 'red')
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
    follower_ids = self.get_user_followers(user_id, nfollows)
    if not follower_ids:
        self.logger.info("{} not found / closed / has no followers.".format(user_id))
    else:
        self.follow_users(follower_ids[:nfollows])


def follow_following(self, user_id, nfollows=None):
    self.logger.info("Follow following of: {}".format(user_id))
    if not limits.check_if_bot_can_follow(self):
        self.logger.info("Out of follows for today.")
        return
    if not user_id:
        self.logger.info("User not found.")
        return
    following_ids = self.get_user_following(user_id)
    if not following_ids:
        self.logger.info("{} not found / closed / has no following.".format(user_id))
    else:
        self.follow_users(following_ids[:nfollows])
