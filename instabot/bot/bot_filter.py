"""
    Filter functions for media and user lists.
"""

from . import delay


# Adding useless userd_ids to the skipped_list file: skipped.txt , so
# InstaBot will not try to follow them again or InstaBot will not like
# their medias anymore
def skippedlist_adder(self, user_id):
    # user_id = self.convert_to_user_id(user_id)
    skipped = self.read_list_from_file("skipped.txt")
    if user_id not in skipped:
        with open('skipped.txt', "a") as file:
            print('\n\033[93m Add user_id %s to skippedlist : skipped.txt ... \033[0m' % user_id)
            # Append user_is to the end of skipped.txt
            file.write(str(user_id) + "\n")
            print('Done adding user_id to skipped.txt')
    return


# filtering medias


def filter_medias(self, media_items, filtration=True, quiet=False, is_comment=False):
    if filtration:
        if not quiet:
            self.logger.info("Received %d medias." % len(media_items))
        if not is_comment:
            media_items = _filter_medias_not_liked(media_items)
            if self.max_likes_to_like:
                media_items = _filter_medias_nlikes(
                    media_items, self.max_likes_to_like)
        else:
            media_items = _filter_medias_not_commented(self, media_items)
        if not quiet:
            self.logger.info("After filtration %d medias left." % len(media_items))
    return _get_media_ids(media_items)


def _filter_medias_not_liked(media_items):
    not_liked_medias = []
    for media in media_items:
        if 'has_liked' in media.keys():
            if not media['has_liked']:
                not_liked_medias.append(media)
    return not_liked_medias


def _filter_medias_not_commented(self, media_items):
    not_commented_medias = []
    for media in media_items:
        if media['comment_count'] > 0:
            my_comments = [comment for comment in media['comments'] if comment['user_id'] == self.user_id]
            if my_comments:
                continue
        not_commented_medias.append(media)
    return not_commented_medias


def _filter_medias_nlikes(media_items, max_likes_to_like):
    filtered_medias = []
    for media in media_items:
        if 'like_count' in media.keys():
            if media['like_count'] < max_likes_to_like:
                filtered_medias.append(media)
    return filtered_medias


def _get_media_ids(media_items):
    result = []
    for m in media_items:
        if 'pk' in m.keys():
            result.append(m['pk'])
    return result


def check_media(self, media_id):
    self.mediaInfo(media_id)
    if len(self.filter_medias(self.LastJson["items"])):
        return check_user(self, self.get_media_owner(media_id))
    else:
        return False

# filter users


def search_stop_words_in_user(self, user_info):
    text = ''
    if 'biography' in user_info:
        text += user_info['biography'].lower()

    if 'username' in user_info:
        text += user_info['username'].lower()

    if 'full_name' in user_info:
        text += user_info['full_name'].lower()

    for stop_word in self.stop_words:
        if stop_word in text:
            return True

    return False


def filter_users(self, user_id_list):
    return [str(user["pk"]) for user in user_id_list]


def check_user(self, user_id, filter_closed_acc=False):
    if not self.filter_users:
        return True

    delay.small_delay(self)
    user_id = self.convert_to_user_id(user_id)

    if not user_id:
        print('\n\033[91m not user_id , Skipping \033[0m')  # Log to Console
        return False
    if self.whitelist and user_id in self.whitelist:
        print('\n\033[92m user_id in self.whitelist \033[0m')  # Log to Console
        return True
    if self.blacklist and user_id in self.blacklist:
        print('\n\033[91m user_id in self.blacklist \033[0m')  # Log to Console
        return False

    if not self.following:
        # Log to Console
        print(
            '\n\033[92m My own following list is empty , downloading ...\033[0m')
        self.following = self.get_user_following(self.user_id)
    if user_id in self.following:
        # Log to Console
        print('\n\033[91m Already following , Skipping \033[0m')
        return False

    user_info = self.get_user_info(user_id)
    if not user_info:
        print('\n\033[91m not user_info , Skipping \033[0m')  # Log to Console
        return False

    print('\n USER_NAME: %s , FOLLOWER: %s , FOLLOWING: %s ' % (user_info[
          "username"], user_info["follower_count"], user_info["following_count"]))  # Log to Console
    if filter_closed_acc and "is_private" in user_info:
        if user_info["is_private"]:
            # Log to Console
            print('\n info : \033[91m is PRIVATE , !!! \033[0m')
            return False
    if "is_business" in user_info:
        if user_info["is_business"]:
            # Log to Console
            print('\n info : \033[91m is BUSINESS , Skipping \033[0m')
            skippedlist_adder(self, user_id)  # Add user_id to skipped.txt
            return False
    if "is_verified" in user_info:
        if user_info["is_verified"]:
            # Log to Console
            print('\n info : \033[91m is VERIFIED , Skipping \033[0m')
            skippedlist_adder(self, user_id)  # Add user_id to skipped.txt
            return False
    if "follower_count" in user_info and "following_count" in user_info:
        if user_info["follower_count"] < self.min_followers_to_follow:
            # Log to Console
            print(
                '\n\033[91m user_info["follower_count"] < self.min_followers_to_follow , Skipping \033[0m')
            skippedlist_adder(self, user_id)  # Add user_id to skipped.txt
            return False
        if user_info["follower_count"] > self.max_followers_to_follow:
            # Log to Console
            print(
                '\n\033[91m user_info["follower_count"] > self.max_followers_to_follow , Skipping \033[0m')
            skippedlist_adder(self, user_id)  # Add user_id to skipped.txt
            return False
        if user_info["following_count"] < self.min_following_to_follow:
            # Log to Console
            print(
                '\n\033[91m user_info["following_count"] < self.min_following_to_follow , Skipping \033[0m')
            skippedlist_adder(self, user_id)  # Add user_id to skipped.txt
            return False
        if user_info["following_count"] > self.max_following_to_follow:
            # Log to Console
            print(
                '\n\033[91m user_info["following_count"] > self.max_following_to_follow , Skipping \033[0m')
            skippedlist_adder(self, user_id)  # Add user_id to skipped.txt
            return False
        try:
            if user_info["follower_count"] / user_info["following_count"] \
                    > self.max_followers_to_following_ratio:
                # Log to Console
                print(
                    '\n\033[91m ["follower_count"] / ["following_count"] > self.max_followers_to_following_ratio , Skipping \033[0m')
                skippedlist_adder(self, user_id)  # Add user_id to skipped.txt
                return False
            if user_info["following_count"] / user_info["follower_count"] \
                    > self.max_following_to_followers_ratio:
                # Log to Console
                print(
                    '\n\033[91m ["following_count"] / ["follower_count"] > self.max_following_to_followers_ratio , Skipping \033[0m')
                skippedlist_adder(self, user_id)  # Add user_id to skipped.txt
                return False
        except ZeroDivisionError:
            print('!!! Exxxcept ZeroDivisionError !!! ')
            return False

    if 'media_count' in user_info:
        if user_info["media_count"] < self.min_media_count_to_follow:
            # Log to Console
            print(
                '\n\033[91m user_info["media_count"] < self.min_media_count_to_follow , BOT or InActive , Skipping \033[0m')
            skippedlist_adder(self, user_id)  # Add user_id to skipped.txt
            return False  # bot or inactive user

    if search_stop_words_in_user(self, user_info):
        # Log to Console
        print('\n\033[91m search_stop_words_in_user , Skipping \033[0m')
        skippedlist_adder(self, user_id)  # Add user_id to skipped.txt
        return False

    return True


def check_not_bot(self, user_id):
    delay.small_delay(self)
    """ Filter bot from real users. """
    user_id = self.convert_to_user_id(user_id)
    if not user_id:
        return False
    if self.whitelist and user_id in self.whitelist:
        return True
    if self.blacklist and user_id in self.blacklist:
        return False

    user_info = self.get_user_info(user_id)
    if not user_info:
        return True  # closed acc

    if "following_count" in user_info:
        if user_info["following_count"] > self.max_following_to_block:
            # Log to Console
            print(
                '\n\033[91m user_info["following_count"] > self.max_following_to_block , Skipping \033[0m')
            skippedlist_adder(self, user_id)  # Add user_id to skipped.txt
            return False  # massfollower

    if search_stop_words_in_user(self, user_info):
        # Log to Console
        print('\n\033[91m search_stop_words_in_user , Skipping \033[0m')
        skippedlist_adder(self, user_id)  # Add user_id to skipped.txt
        return False

    return True
