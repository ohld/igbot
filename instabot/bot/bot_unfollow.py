from tqdm import tqdm

from . import limits
from . import delay


def unfollow(self, user_id):
    user_id = self.convert_to_user_id(user_id)
    user_info = self.get_user_info(user_id)
    self.console_print('\n===> Going to UN-Follow user_id: %s , user_name: %s'
                       % (user_id, user_info["username"]))

    if self.check_user(user_id, unfollowing=True):
        return True  # whitelisted user
    if limits.check_if_bot_can_unfollow(self):
        delay.unfollow_delay(self)
        if super(self.__class__, self).unfollow(user_id):
            self.console_print('\033[93m===> UN-FOLLOWED , user_id: %s , user_name: %s \033[0m\n' % (
                               user_id, user_info["username"]))
            self.total_unfollowed += 1
            return True
    else:
        self.logger.info("Out of unfollows for today.")
    return False


def unfollow_users(self, user_ids):
    broken_items = []
    self.logger.info("Going to unfollow %d users." % len(user_ids))
    user_ids = set(map(str, user_ids))
    filtered_user_ids = list(set(user_ids) - set(self.whitelist))
    if len(filtered_user_ids) != len(user_ids):
        self.logger.info(
            "After filtration by whitelist %d users left." % len(filtered_user_ids))
    for user_id in tqdm(filtered_user_ids, desc='Processed users'):
        if not self.unfollow(user_id):
            delay.error_delay(self)
            broken_items = filtered_user_ids[filtered_user_ids.index(user_id):]
            break
    self.logger.info("DONE: Total unfollowed %d users. " %
                     self.total_unfollowed)
    return broken_items


def unfollow_non_followers(self, n_to_unfollows=None):
    self.logger.info("Unfollowing non-followers")
    self.update_unfollow_file()
    self.console_print("\n\033[91m ===> Start Unfollowing Non_Followers List <===\033[0m")

    unfollow_file = "unfollow.txt"
    with open(unfollow_file) as unfollow_data:
        new_unfollow_list = list(line.strip() for line in unfollow_data)
    for user in tqdm(new_unfollow_list[:n_to_unfollows]):  # select only first n_to_unfollows users to unfollow
        self.unfollow(user)
    self.console_print("\n\033[91m ===> Unfollow Non_followers , Task Done <===\033[0m")


def unfollow_everyone(self):
    self.following = self.get_user_following(self.user_id)
    self.unfollow_users(self.following)


def update_unfollow_file(self):  # Update unfollow.txt
    self.logger.info("Updating unfollow.txt ...")
    self.console_print("\n\033[92m Calculating Non Followers List  \033[0m")

    followings = self.get_user_following(self.user_id)  # getting following
    followers = self.get_user_followers(self.user_id)  # getting followers
    friends_file = self.read_list_from_file(
        "friends.txt")  # same whitelist (just user ids)
    nonfollowerslist = list(
        (set(followings) - set(followers)) - set(friends_file))
    followed_file = "followed.txt"
    followed_list = self.read_list_from_file(followed_file)
    unfollow_list = []
    unfollow_list += [x for x in followed_list if x in nonfollowerslist]
    unfollow_list += [x for x in nonfollowerslist if x not in followed_list]
    unfollow_file = self.read_list_from_file("unfollow.txt")
    new_unfollow_list = []
    new_unfollow_list += [x for x in unfollow_file if x in unfollow_list]
    new_unfollow_list += [x for x in unfollow_list if x not in unfollow_file]

    self.console_print("\n Writing to unfollow.txt")
    with open('unfollow.txt', 'w') as out:
        for line in new_unfollow_list:
            out.write(str(line) + "\n")
    self.console_print("\n Updating unfollow.txt , Task Done")
