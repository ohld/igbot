from tqdm import tqdm

from . import limits
from . import delay


def follow(self, user_id):
    user_id = self.convert_to_user_id(user_id)
    print('\n ===> Going to Follow user_id: %s ' % (user_id))  # Log to console
    if not self.check_user(user_id):
        return True
    if limits.check_if_bot_can_follow(self):
        delay.follow_delay(self)
        if super(self.__class__, self).follow(user_id):
            print('\n\033[92m ===> FOLLOWED <==== user_id: %s \033[0m' % (
                user_id))  # Log to console
            self.total_followed += 1
            # Log to console
            print(
                '\n\033[92m Writing user_id to file : followed.txt ... \033[0m')
            with open('followed.txt', 'a') as file:  # Appending user_id to the followed.txt
                # Appending user_id to the followed.txt
                file.write(str(user_id) + "\n")
            return True
    else:
        self.logger.info("Out of follows for today.")
    return False


def follow_users(self, user_ids):
    broken_items = []
    if not limits.check_if_bot_can_follow(self):
        self.logger.info("Out of follows for today.")
        return
    self.logger.info("Going to follow %d users." % len(user_ids))
    followed_list = self.read_list_from_file(
        "followed.txt")   # Read followed.txt file
    skipped_list = self.read_list_from_file(
        "skipped.txt")  # Read skipped.txt file
    print('\n\033[92m Going to follow %s user_ids ...\033[0m' %
          len(user_ids))  # Log to console
    # remove skipped and followed list from user_ids
    user_ids = list((set(user_ids) - set(followed_list)) - set(skipped_list))
    print('\n\033[92m After filtering followedlist.txt and skippedlist.txt, [ %s ] user_ids left to follow. \033[0m' % len(
        user_ids))  # Log to console
    for user_id in tqdm(user_ids):
        if not self.follow(user_id):
            delay.error_delay(self)
            broken_items = user_ids[user_ids.index(user_id):]
            break
    self.logger.info("DONE: Total followed %d users." % self.total_followed)
    return broken_items


def follow_followers(self, user_id, nfollows=None):
    self.logger.info("Follow followers of: %s" % user_id)
    if not limits.check_if_bot_can_follow(self):
        self.logger.info("Out of follows for today.")
        return
    if not user_id:
        self.logger.info("User not found.")
        return
    follower_ids = self.get_user_followers(user_id, nfollows)
    if not follower_ids:
        self.logger.info("%s not found / closed / has no followers." % user_id)
    else:
        self.follow_users(follower_ids[:nfollows])


def follow_following(self, user_id, nfollows=None):
    self.logger.info("Follow following of: %s" % user_id)
    if not limits.check_if_bot_can_follow(self):
        self.logger.info("Out of follows for today.")
        return
    if not user_id:
        self.logger.info("User not found.")
        return
    following_ids = self.get_user_following(user_id)
    if not following_ids:
        self.logger.info("%s not found / closed / has no following." % user_id)
    else:
        self.follow_users(following_ids[:nfollows])
