"""
    All methods must return media_ids that can be
    passed into e.g. like() or comment() functions.
"""

import time
import random
from . import limits

# filters

def filter_not_liked(media_items, log=False):
    # TODO: convert these print function to logging

    not_liked_medias = []
    for m in media_items:
        if 'pk' in m.keys():
            if 'has_liked' in m.keys():
                if not m['has_liked']:
                    if m['like_count'] <= limits.MAX_LIKES_TO_LIKE:
                        not_liked_medias.append(m['pk'])
    if log:
        print ("  Recieved: %d. Already liked: %d." % (
                            len(media_items),
                            len(media_items) - len(not_liked_medias)
                            )
        )
    return not_liked_medias

def filter_media(media_items, log=False):
    # TODO: should return not liked and not commented medias
    # remove filter_not_liked when implemented
    return filter_not_liked(media_items, log=False)

def filter_users(user_items, log=False):
    # TODO: filter users from blacklist and already subscribed
    pass

# getters

def get_timeline_medias(self):
    if not self.getTimelineFeed():
        self.logger.info("  Error while getting timeline feed")
        return False
    return filter_media(self.LastJson["items"])

def get_user_medias(self, user_id):
    self.getUserFeed(user_id)
    if self.LastJson["status"] == 'fail':
        self.logger.info("  This is a closed account")
        return False
    return filter_media(self.LastJson["items"])

def get_hashtag_medias(self, hashtag):
    if not self.getHashtagFeed(hashtag):
         self.logger.info("Error while getting hashtag feed")
         return False
    return filter_media(self.LastJson["items"])

def get_geotag_medias(self, geotag):
    # TODO: returns list of medias from geotag
    pass

def get_timeline_users(self):
    # TODO: returns list userids who just posted on your timeline feed
    pass

def get_hashtag_users(self, hashtag):
    # TODO: returns list userids who just posted on this hashtag
    pass

def get_geotag_users(self, geotag):
    # TODO: returns list userids who just posted on this geotag
    pass

def get_userid_from_username(self, username):
    # TODO:
    pass

def get_user_followers(self, user_id):
    # TODO: return a list of user's followers
    pass

def get_user_following(self, user_id):
    # TODO: return a list of user's following
    pass

def get_media_likers(self, media_id):
    # TODO:
    pass

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
