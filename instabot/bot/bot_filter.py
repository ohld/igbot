"""
    Filter functions for media and user lists.
"""

from . import delay
from ..api import api_db


# Adding useless userd_ids to the skipped_list file: skipped.txt , so
# InstaBot will not try to follow them again or InstaBot will not like
# their medias anymore
# TODO if needed save the data in db
def skippedlist_adder(self, user_id):
    return False
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

# this is used to remove medias already liked  and to remove medias which have more likes then max_likes_to_like parameter
#TODO remove self medias
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

    # TODO fix this for all calls
    # return _get_media_ids(media_items)
    return media_items


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


def check_user(self, user, filter_closed_acc=False):
    user_id = user['instagram_id_user']

    #self.logger.info("Going to check user %s id: %s if worth liking/following", user['full_name'], user_id)

    # delay.small_delay(self)

    if not user_id:
        self.logger.info('Invalid user_id, skipping')
        return False

    user_info = self.get_user_info(user_id)
    if not user_info:
        self.logger.info('Error: Could not retrieve user info , Skipping')
        return False

    #self.logger.info('USER_NAME: %s , FOLLOWER: %s , FOLLOWING: %s  MEDIA %s' % (user_info[
    #                                                                        "username"], user_info["follower_count"],
    #                                                                    user_info["following_count"], user_info['media_count']))

    #print('\n USER_NAME: %s , FOLLOWER: %s , FOLLOWING: %s ' % (user_info[
    #                                                                "username"], user_info["follower_count"],
    #                                                            user_info["following_count"]))  # Log to Console

    #skip private user
    if "is_private" in user_info:
        if user_info["is_private"]:
            self.logger.info('USER IS PRIVATE')
            return False

    if "follower_count" in user_info:
        if user_info["follower_count"] < self.min_followers_to_follow:
            self.logger.info('SKIPPING: user_info["follower_count"] < self.min_followers_to_follow , Skipping %s vs %s' % (user_info["follower_count"], self.min_followers_to_follow))
            return False

    if "following_count" in user_info:
        if user_info["following_count"] < self.min_following_to_follow:
            self.logger.info('\n\033[91m SKIPPING: user_info["following_count"] < self.min_following_to_follow , Skipping %s vs %s \033[0m' % (user_info['following_count'], self.min_following_to_follow))
            return False

    if 'media_count' in user_info:
        if user_info["media_count"] < self.min_media_count_to_follow:
            # Log to Console
            self.logger.info('SKIPPING: user_info["media_count"] < self.min_media_count_to_follow , BOT or InActive , Skipping %s vs %s' % (user_info['media_count'], self.min_media_count_to_follow))
            return False  # bot or inactive user

    #if search_stop_words_in_user(self, user_info):
        # Log to Console
    #    self.logger.info('\n\033[91m search_stop_words_in_user , Skipping \033[0m')
    #    return False

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
            self.logger.info(
                '\n\033[91m user_info["following_count"] > self.max_following_to_block , Skipping \033[0m')
            skippedlist_adder(self, user_id)  # Add user_id to skipped.txt
            return False  # massfollower

    if search_stop_words_in_user(self, user_info):
        # Log to Console
        self.logger.info('\n\033[91m search_stop_words_in_user , Skipping \033[0m')
        skippedlist_adder(self, user_id)  # Add user_id to skipped.txt
        return False

    return True
