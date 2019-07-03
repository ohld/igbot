from tqdm import tqdm


def unfollow(self, user_id):
    user_id = self.convert_to_user_id(user_id)
    user_info = self.get_user_info(user_id)
    username = user_info.get("username")
    self.console_print('===> Going to unfollow `user_id`: {} with username: {}'.format(user_id, username))

    if self.check_user(user_id, unfollowing=True):
        return True  # whitelisted user
    if not self.reached_limit('unfollows'):
        self.delay('unfollow')
        if self.api.unfollow(user_id):
            msg = '===> Unfollowed, `user_id`: {}, user_name: {}'
            self.console_print(msg.format(user_id, username), 'yellow')
            self.unfollowed_file.append(user_id)
            self.total['unfollows'] += 1
            if user_id in self.following:
                self.following.remove(user_id)
            return True
    else:
        self.logger.info("Out of unfollows for today.")
    return False


def unfollow_users(self, user_ids):
    broken_items = []
    self.logger.info("Going to unfollow {} users.".format(len(user_ids)))
    user_ids = set(map(str, user_ids))
    filtered_user_ids = list(set(user_ids) - set(self.whitelist))
    if len(filtered_user_ids) != len(user_ids):
        self.logger.info(
            "After filtration by whitelist {} users left.".format(len(filtered_user_ids)))
    for user_id in tqdm(filtered_user_ids, desc='Processed users'):
        if not self.unfollow(user_id):
            self.error_delay()
            i = filtered_user_ids.index(user_id)
            broken_items = filtered_user_ids[i:]
            break
    self.logger.info("DONE: Total unfollowed {} users.".format(self.total['unfollows']))
    return broken_items


def unfollow_non_followers(self, n_to_unfollows=None):
    self.logger.info("Unfollowing non-followers.")
    self.console_print(" ===> Start unfollowing non-followers <===", 'red')
    non_followers = set(self.following) - set(self.followers) - self.friends_file.set
    non_followers = list(non_followers)
    for user_id in tqdm(non_followers[:n_to_unfollows]):
        if self.reached_limit('unfollows'):
            self.logger.info("Out of unfollows for today.")
            break
        self.unfollow(user_id)
    self.console_print(" ===> Unfollow non-followers done! <===", 'red')


def unfollow_everyone(self):
    self.unfollow_users(self.following)
