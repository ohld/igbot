"""
    All methods must return media_ids that can be
    passed into e.g. like() or comment() functions.
"""

import random
from tqdm import tqdm

from . import delay


def get_media_owner(self, media_id):
    self.mediaInfo(media_id)
    try:
        return str(self.LastJson["items"][0]["user"]["pk"])
    except:
        return False


def get_popular_medias(self):
    self.getPopularFeed()
    return [str(media['pk']) for media in self.LastJson['items']]


def get_your_medias(self, as_dict=False):
    self.getSelfUserFeed()
    if as_dict:
        return self.LastJson["items"]
    return self.filter_medias(self.LastJson["items"], False)


def get_archived_medias(self, as_dict=False):
    self.getArchiveFeed()
    if as_dict:
        return self.LastJson["items"]
    return self.filter_medias(self.LastJson["items"], False)


def get_timeline_medias(self, filtration=True):
    if not self.getTimelineFeed():
        self.logger.warning("Error while getting timeline feed.")
        return []
    return self.filter_medias(self.LastJson["items"], filtration)


def get_user_medias(self, user_id, filtration=True, is_comment=False):
    user_id = self.convert_to_user_id(user_id)
    self.getUserFeed(user_id)
    if self.LastJson["status"] == 'fail':
        self.logger.warning("This is a closed account.")
        return []
    return self.filter_medias(self.LastJson["items"], filtration, is_comment=is_comment)


def get_total_user_medias(self, user_id):
    user_id = self.convert_to_user_id(user_id)
    medias = self.getTotalUserFeed(user_id)
    if self.LastJson["status"] == 'fail':
        self.logger.warning("This is a closed account.")
        return []
    return self.filter_medias(medias, filtration=False)


def get_user_likers(self, user_id, media_count=10):
    your_likers = set()
    media_items = self.get_user_medias(user_id, filtration=False)
    if not media_items:
        self.logger.warning("Can't get %s medias." % user_id)
        return []
    for media_id in tqdm(media_items[:media_count],
                         desc="Getting %s media likers" % user_id):
        media_likers = self.get_media_likers(media_id)
        your_likers |= set(media_likers)
    return list(your_likers)


def get_hashtag_medias(self, hashtag, filtration=True):
    if not self.getHashtagFeed(hashtag):
        self.logger.warning("Error while getting hashtag feed.")
        return []
    return self.filter_medias(self.LastJson["items"], filtration)


def get_geotag_medias(self, geotag, filtration=True):
    # TODO: returns list of medias from geotag
    pass


def get_locations_from_coordinates(self, latitude, longitude):
    self.searchLocation(lat=latitude, lng=longitude)
    return [location for location in self.LastJson["items"] if int(location["location"]["lat"]) == int(latitude) and
            int(location["location"]["lng"]) == int(longitude)]


def get_media_info(self, media_id):
    if isinstance(media_id, dict):
        return media_id
    self.mediaInfo(media_id)
    if "items" not in self.LastJson:
        self.logger.info("Media with %s not found." % media_id)
        return []
    return self.LastJson["items"]


def get_timeline_users(self):
    # TODO: returns list userids who just posted on your timeline feed
    if not self.getTimelineFeed():
        self.logger.warning("Error while getting timeline feed.")
        return []
    return [str(i['user']['pk']) for i in self.LastJson['items'] if i.get('user')]


def get_hashtag_users(self, hashtag):
    users = []
    self.getHashtagFeed(hashtag)
    for i in self.LastJson['items']:
        users.append(str(i['user']['pk']))
    return users


def get_geotag_users(self, geotag):
    # TODO: returns list userids who just posted on this geotag
    pass


def get_userid_from_username(self, username):
    self.searchUsername(username)
    if "user" in self.LastJson:
        return str(self.LastJson["user"]["pk"])
    return None  # Not found


def get_username_from_userid(self, userid):
    self.getUsernameInfo(userid)
    if "user" in self.LastJson:
        return str(self.LastJson["user"]["username"])
    return None  # Not found


def get_user_info(self, user_id):
    user_id = self.convert_to_user_id(user_id)
    self.getUsernameInfo(user_id)
    if 'user' not in self.LastJson:
        return False
    return self.LastJson['user']


def get_user_followers(self, user_id, nfollows):
    user_id = self.convert_to_user_id(user_id)
    followers = self.getTotalFollowers(user_id, nfollows)
    return [str(item['pk']) for item in followers][::-1] if followers else []


def get_user_following(self, user_id, nfollows=None):
    user_id = self.convert_to_user_id(user_id)
    following = self.getTotalFollowings(user_id, nfollows)
    return [str(item['pk']) for item in following][::-1] if following else []


def get_media_likers(self, media_id):
    self.getMediaLikers(media_id)
    if "users" not in self.LastJson:
        self.logger.info("Media with %s not found." % media_id)
        return []
    return list(map(lambda user: str(user['pk']), self.LastJson["users"]))


def get_media_comments(self, media_id, only_text=False):
    self.getMediaComments(media_id)
    if 'comments' not in self.LastJson:
        return []
    if only_text:
        return [str(item["text"]) for item in self.LastJson['comments']]
    return self.LastJson['comments']


def get_media_commenters(self, media_id):
    self.getMediaComments(media_id)
    if 'comments' not in self.LastJson:
        return []
    return [str(item["user"]["pk"]) for item in self.LastJson['comments']]


def get_comment(self):
    if len(self.comments):
        return random.choice(self.comments).strip()
    return "wow"


def convert_to_user_id(self, smth):
    smth = str(smth)
    if not smth.isdigit():
        if smth[0] == "@":  # cut first @
            smth = smth[1:]
        smth = self.get_userid_from_username(smth)
        delay.very_small_delay(self)
    # if type is not str than it is int so user_id passed
    return smth
