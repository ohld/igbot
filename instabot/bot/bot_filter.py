"""
    Filter functions for media and user lists.
"""

# filtering medias


def filter_medias(self, media_items, filtration=True):
    if filtration:
        self.logger.info("Recieved %d medias." % len(media_items))
        media_items = _filter_medias_not_liked(media_items)
        if self.max_likes_to_like:
            media_items = _filter_medias_nlikes(
                media_items, self.max_likes_to_like)
        self.logger.info("After filtration %d medias left." % len(media_items))
    return _get_media_ids(media_items)


def _filter_medias_not_liked(media_items):
    not_liked_medias = []
    for media in media_items:
        if 'has_liked' in media.keys():
            if not media['has_liked']:
                not_liked_medias.append(media)
    return not_liked_medias


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


def filter_users(self, user_id_list):
    return [user["pk"] for user in user_id_list]


def check_user(self, user_id):
    user_id = self.convert_to_user_id(user_id)

    if not user_id:
        return True
    if self.whitelist and user_id in self.whitelist:
        return True
    if self.blacklist and user_id in self.blacklist:
        return False

    user_info = self.get_user_info(user_id)
    if not user_info:
        return True  # closed acc
    if "is_business" in user_info:
        if user_info["is_business"]:
            return False
    if "is_verified" in user_info:
        if user_info["is_verified"]:
            return False
    if "follower_count" in user_info and "following_count" in user_info:
        if user_info["follower_count"] < 100:
            return True  # not famous user
        if user_info["following_count"] < 10:
            return False
        if user_info["follower_count"] / user_info["following_count"] > 10:
            return False  # too many
        if user_info["following_count"] / user_info["follower_count"] > 2:
            return True  # too many
    if 'media_count' in user_info:
        if user_info["media_count"] < 3:
            return False  # bot or inactive user
    return True
