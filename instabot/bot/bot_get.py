"""
    All methods must return media_ids that can be
    passed into e.g. like() or comment() functions.
"""

import random

# filters

def get_media_ids(media_items):
    result = []
    for m in media_items:
        if 'pk' in m.keys():
            result.append(m['pk'])
    return result

def filter_not_liked(media_items, log=False):
    not_liked_medias = []
    for m in media_items:
        if 'has_liked' in m.keys():
            if not m['has_liked']:
                not_liked_medias.append(m)
    return not_liked_medias

def filter_nlikes(media_items, max_likes_to_like, log=False):
    filtered_medias = []
    for m in media_items:
        if 'like_count' in m.keys():
            if m['like_count'] < max_likes_to_like:
                filtered_medias.append(m)
    return filtered_medias

def filter_media(bot, media_items, log=False):
    media_items = filter_not_liked(media_items)
    media_items = filter_nlikes(media_items, bot.max_likes_to_like)
    return get_media_ids(media_items)

# getters

def get_your_medias(self):
    self.getSelfUserFeed()
    return [item["pk"] for item in self.LastJson["items"]]

def get_timeline_medias(self):
    if not self.getTimelineFeed():
        self.logger.info("Error while getting timeline feed.")
        return False
    return filter_media(self, self.LastJson["items"])

def get_user_medias(self, user_id):
    user_id = self.convert_to_user_id(user_id)
    self.getUserFeed(user_id)
    if self.LastJson["status"] == 'fail':
        self.logger.info("This is a closed account.")
        return False
    return filter_media(self, self.LastJson["items"])

def get_hashtag_medias(self, hashtag):
    if not self.getHashtagFeed(hashtag):
         self.logger.info("Error while getting hashtag feed.")
         return False
    return filter_media(self, self.LastJson["items"])

def get_geotag_medias(self, geotag):
    # TODO: returns list of medias from geotag
    pass

def get_timeline_users(self):
    # TODO: returns list userids who just posted on your timeline feed
    pass

def get_hashtag_users(self, hashtag):
    users = []
    self.getHashtagFeed(hashtag)
    for i in self.LastJson['items']:
        users.append(i['user']['pk'])
    return users

def get_geotag_users(self, geotag):
    # TODO: returns list userids who just posted on this geotag
    pass

def get_userid_from_username(self, username):
    self.searchUsername(username)
    if "user" in self.LastJson:
        return str(self.LastJson["user"]["pk"])
    return None # Not found

def get_user_info(self, user_id):
    user_id = self.convert_to_user_id(user_id)
    self.getUsernameInfo(user_id)
    if 'user' not in self.LastJson:
        return False
    return self.LastJson['user']

def get_user_followers(self, user_id):
    user_id = self.convert_to_user_id(user_id)
    followers = self.getTotalFollowers(user_id)
    return [item['pk'] for item in followers] if followers else False

def get_user_following(self, user_id):
    user_id = self.convert_to_user_id(user_id)
    following = self.getTotalFollowings(user_id)
    return [item['pk'] for item in following] if following else False

def get_media_likers(self, media_id):
    self.getMediaLikers(media_id)
    if "users" not in self.LastJson:
        self.logger.info("Media with %s not found." % media_id)
        return False
    return [item['pk'] for item in self.LastJson["users"]]

def get_media_comments(self, media_id):
    # TODO:
    pass

def get_media_commenters(self, media_id):
    self.getMediaComments(media_id)
    if 'comments' not in self.LastJson:
        return []
    return [item["user"]["username"] for item in self.LastJson['comments']]

def get_comment(self):
    if len(self.comments):
        return random.choice(self.comments).strip()
    return "lol"
