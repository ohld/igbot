from tqdm import tqdm

from . import delay, limits


def unfollow(self, user_id):
    user_id = self.convert_to_user_id(user_id)
    user_info = self.get_user_info(user_id)
    username = user_info["username"]
    self.console_print('===> Going to unfollow `user_id`: {} with username: {}'.format(user_id, username))

    if self.check_user(user_id, unfollowing=True):
        return True  # whitelisted user
    if limits.check_if_bot_can_unfollow(self):
        delay.unfollow_delay(self)
        if super(self.__class__, self).unfollow(user_id):
            msg = '===> Unfollowed, `user_id`: {}, user_name: {}}'
            self.console_print(msg.format(user_id, username), 'yellow')
            self.total_unfollowed += 1
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
            delay.error_delay(self)
            i = filtered_user_ids.index(user_id)
            broken_items = filtered_user_ids[i:]
            break
    self.logger.info("DONE: Total unfollowed {} users.".format(self.total_unfollowed))
    return broken_items


def unfollow_non_followers(self, n_to_unfollows=None):
    self.logger.info("Unfollowing non-followers.")
    self.update_unfollow_file()
    self.console_print(" ===> Start unfollowing non-followers <===", 'red')

    unfollow_file = "unfollowed.txt"
    with open(unfollow_file) as unfollow_data:
        new_unfollow_list = list(line.strip() for line in unfollow_data)
    for user in tqdm(new_unfollow_list[:n_to_unfollows]):  # select only first n_to_unfollows users to unfollow
        self.unfollow(user)
    self.console_print(" ===> Unfollow non-followers done! <===", 'red')


def unfollow_everyone(self):
    self.following = self.get_user_following(self.user_id)
    self.unfollow_users(self.following)


def update_unfollow_file(self):  # Update unfollowed.txt
    self.logger.info("Updating `unfollowed.txt`.")
    self.console_print("Calculating non-followers List", 'green')

    followings = self.get_user_following(self.user_id)  # getting following
    followers = self.get_user_followers(self.user_id)  # getting followers
    friends_file = self.read_list_from_file("friends.txt")  # same whitelist (just user ids)
    nonfollowerslist = list((set(followings) - set(followers)) - set(friends_file))
    followed_list = self.read_list_from_file("followed.txt")
    unfollow_list = [x for x in followed_list if x in nonfollowerslist]
    unfollow_list += [x for x in nonfollowerslist if x not in followed_list]
    unfollow_file = self.read_list_from_file("unfollowed.txt")
    new_unfollow_list = [x for x in unfollow_file if x in unfollow_list]
    new_unfollow_list += [x for x in unfollow_list if x not in unfollow_file]

    self.console_print("Adding to `unfollowed.txt`")
    with open('unfollowed.txt', 'w') as out:
        for line in new_unfollow_list:
            out.write(str(line) + "\n")
    self.console_print("Updating unfollowed.txt , Task Done")
