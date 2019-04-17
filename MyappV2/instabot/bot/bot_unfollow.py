from tqdm import tqdm


def unfollow(self, user_id):
    user_id = self.convert_to_user_id(user_id)
    user_info = self.get_user_info(user_id)
    username = user_info["username"]
    # self.console_print('Going to unfollow `user_id`: {} with username: {}'.format(user_id, username))

    if self.check_user(user_id, unfollowing=True):
        return True  # whitelisted user
    if not self.reached_limit('unfollows'):
        self.delay('unfollow')
        if self.api.unfollow(user_id):
            msg = 'UNFOLLOW: https://instagram.com/{}'
            self.console_print(msg.format(username))
            self.unfollowed_file.append(user_id)
            self.total['unfollows'] += 1
            if user_id in self.following:
                self.following.remove(user_id)
            return True
    else:
        self.logger.info("Reach Unfollow limit for today.")
    return False


def unfollow_users(self, user_ids):
    broken_items = []
    self.logger.info("Will unfollow {} users.".format(len(user_ids)))
    user_ids = set(map(str, user_ids))
    filtered_user_ids = list(set(user_ids) - set(self.whitelist))
    if len(filtered_user_ids) != len(user_ids):
        # self.logger.info(
        #     "After filtration {} users left.".format(len(filtered_user_ids)))
        pass
    for user_id in tqdm(filtered_user_ids, desc='Processed users'):
        if not self.unfollow(user_id):
            self.error_delay()
            i = filtered_user_ids.index(user_id)
            broken_items = filtered_user_ids[i:]
            break
    self.logger.info("DONE: Unfollow {} users.".format(self.total['unfollows']))
    return broken_items


def unfollow_non_followers(self, n_to_unfollows=None):
    self.logger.info("Unfollowing non followers.")
    # self.console_print(" Start unfollowing non followers", 'red')
    non_followers = set(self.following) - set(self.followers) - self.friends_file.set
    non_followers = list(non_followers)
    for user_id in tqdm(non_followers[:n_to_unfollows]):
        if self.reached_limit('unfollows'):
            self.logger.info("Reach Unfollow limit for today.")
            break
        self.unfollow(user_id)
    self.console_print("DONE: Unfollow non followers")


def unfollow_everyone(self):
    self.unfollow_users(self.following)
