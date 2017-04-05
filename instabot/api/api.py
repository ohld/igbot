import requests
import json
import hashlib
import hmac
import urllib
import uuid
import sys
import logging
import time
from tqdm import tqdm

from ..user import User

from . import config
from .api_photo import configurePhoto
from .api_photo import uploadPhoto

from .api_search import fbUserSearch
from .api_search import searchUsers
from .api_search import searchUsername
from .api_search import searchTags
from .api_search import searchLocation

from .api_profile import removeProfilePicture
from .api_profile import setPrivateAccount
from .api_profile import setPublicAccount
from .api_profile import getProfileData
from .api_profile import editProfile
from .api_profile import setNameAndPhone

from .prepare import get_credentials
from .prepare import delete_credentials


# The urllib library was split into other modules from Python 2 to Python 3
if sys.version_info.major == 3:
    import urllib.parse


class API(object):

    def __init__(self, username=None, password=None, proxy=None):
        self.User = get_credentials(username, password)
        if not self.User.api_is_set:
            self.User.counters.requests = 0
            self.User.api_is_set = True

        self.User.device_id = self.generateDeviceId(self.User.username,
                                                    self.User.password)
        self.User.uuid = self.generateUUID()
        self.User.isLoggedIn = False
        self.User.proxy = proxy
        self.User.session = requests.Session()
        if self.User.proxy is not None:
            proxies = {
                'http': 'http://' + self.User.proxy,
                'https': 'http://' + self.User.proxy,
            }
            self.User.session.proxies.update(proxies)

        # handle logging
        self.logger = self.set_logger()
        if not self.login():
            warning.warn("Can't login %s." % username)

    @staticmethod
    def set_logger():
        logger = logging.getLogger('instabot')
        logger.setLevel(logging.DEBUG)
        logging.basicConfig(format='%(asctime)s %(message)s',
                            filename='instabot.log',
                            level=logging.WARNING
                            )
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    @staticmethod
    def generateDeviceId(username, password):
        m = hashlib.md5()
        m.update(username.encode('utf-8') + password.encode('utf-8'))
        seed = m.hexdigest()
        volatile_seed = "12345"
        m = hashlib.md5()
        m.update(seed.encode('utf-8') + volatile_seed.encode('utf-8'))
        return 'android-' + m.hexdigest()[:16]

    @staticmethod
    def generateUUID():
        generated_uuid = str(uuid.uuid4())
        return generated_uuid

    def login(self, force=False):
        if not force and self.User.isLoggedIn:
            return True
        if (
            self.SendRequest('si/fetch_headers/?challenge_type=signup&guid=' + self.User.uuid.replace('-', ''),
                             None, True)):

            data = {'phone_id': self.User.uuid,
                    '_csrftoken': self.LastResponse.cookies['csrftoken'],
                    'username': self.User.username,
                    'guid': self.User.uuid,
                    'device_id': self.User.device_id,
                    'password': self.User.password,
                    'login_attempt_count': '0'}

            if self.SendRequest('accounts/login/', self.generateSignature(json.dumps(data)), True):
                self.User.user_id = self.LastJson["logged_in_user"]["pk"]
                self.User.rank_token = "%s_%s" % (
                    self.User.user_id, self.User.uuid)
                self.User.token = self.LastResponse.cookies["csrftoken"]

                self.logger.info("Login success as %s!" %
                                 self.User.username)
                self.User.isLoggedIn = True
                return True
            else:
                self.logger.warning(
                    "Login or password is incorrect or you need to approve "
                    "Pyour actions in Instagram App. Go there and check that all is ok.")
                self.User.isLoggedIn = False
                time.sleep(30)
                self.login()
        else:
            self.logger.warning(
                "Can't login. May be you have been banned. Go to mobile app and try again.")
            delete_credentials(self.User.username)
            exit()

    def logout(self):
        if not self.User.isLoggedIn:
            return True
        self.User.isLoggedIn = not self.SendRequest('accounts/logout/')
        self.User.save()
        return not self.User.isLoggedIn

    def SendRequest(self, endpoint, post=None, login=False):
        if (not self.User.isLoggedIn and not login):
            self.logger.critical("Not logged in.")
            raise Exception("Not logged in!")

        self.User.session.headers.update({'Connection': 'close',
                                          'Accept': '*/*',
                                          'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                          'Cookie2': '$Version=1',
                                          'Accept-Language': 'en-US',
                                          'User-Agent': config.USER_AGENT})
        try:
            self.User.counters.requests += 1
            if post is not None:  # POST
                response = self.User.session.post(
                    config.API_URL + endpoint, data=post)
            else:  # GET
                response = self.User.session.get(
                    config.API_URL + endpoint)
        except Exception as e:
            self.logger.warning(str(e))
            return False

        if response.status_code == 200:
            self.LastResponse = response
            self.LastJson = json.loads(response.text)
            return True
        else:
            self.logger.warning("Request return " +
                                str(response.status_code) + " error!")
            if response.status_code == 429:
                sleep_minutes = 5
                self.logger.warning("That means 'too many requests'. "
                                    "I'll go to sleep for %d minutes." % sleep_minutes)
                time.sleep(sleep_minutes * 60)

            # for debugging
            try:
                self.LastResponse = response
                self.LastJson = json.loads(response.text)
            except:
                pass
            return False

    def data_to_send_with(self, items):
        base_dict = {
            '_uuid': self.User.uuid,
            '_uid': self.User.user_id,
            '_csrftoken': self.User.token,
        }
        base_dict.update(items)
        return json.dumps(base_dict)

    def syncFeatures(self):
        data = self.data_to_send_with({
            'id': self.User.user_id,
            'experiments': config.EXPERIMENTS
        })
        return self.SendRequest('qe/sync/', self.generateSignature(data))

    def autoCompleteUserList(self):
        return self.SendRequest('friendships/autocomplete_user_list/')

    def getTimelineFeed(self):
        """ Returns 8 medias from timeline feed of logged user """
        return self.SendRequest('feed/timeline/')

    def megaphoneLog(self):
        return self.SendRequest('megaphone/log/')

    def expose(self):
        data = self.data_to_send_with({
            'id': self.User.user_id,
            'experiment': 'ig_android_profile_contextual_feed'
        })
        return self.SendRequest('qe/expose/', self.generateSignature(data))

    def uploadPhoto(self, photo, caption=None, upload_id=None):
        return uploadPhoto(self, photo, caption, upload_id)

    def configurePhoto(self, upload_id, photo, caption=''):
        return configurePhoto(self, upload_id, photo, caption)

    def editMedia(self, mediaId, captionText=''):
        data = self.data_to_send_with({'caption_text': captionText})
        return self.SendRequest('media/' + str(mediaId) + '/edit_media/', self.generateSignature(data))

    def removeSelftag(self, mediaId):
        data = self.data_to_send_with({})
        return self.SendRequest('media/' + str(mediaId) + '/remove/', self.generateSignature(data))

    def mediaInfo(self, mediaId):
        data = self.data_to_send_with({
            'media_id': mediaId
        })
        return self.SendRequest('media/' + str(mediaId) + '/info/', self.generateSignature(data))

    def deleteMedia(self, mediaId):
        data = self.data_to_send_with({
            'media_id': mediaId
        })
        return self.SendRequest('media/' + str(mediaId) + '/delete/', self.generateSignature(data))

    def changePassword(self, newPassword):
        data = self.data_to_send_with({
            'old_password': self.User.password,
            'new_password1': newPassword,
            'new_password2': newPassword
        })
        return self.SendRequest('accounts/change_password/', self.generateSignature(data))

    def explore(self):
        return self.SendRequest('discover/explore/')

    def comment(self, mediaId, commentText):
        data = self.data_to_send_with({
            'comment_text': commentText
        })
        return self.SendRequest('media/' + str(mediaId) + '/comment/', self.generateSignature(data))

    def deleteComment(self, mediaId, commentId):
        data = self.data_to_send_with({})
        return self.SendRequest('media/' + str(mediaId) + '/comment/' + str(commentId) + '/delete/',
                                self.generateSignature(data))

    def removeProfilePicture(self):
        return removeProfilePicture(self)

    def setPrivateAccount(self):
        return setPrivateAccount(self)

    def setPublicAccount(self):
        return setPublicAccount(self)

    def getProfileData(self):
        return getProfileData(self)

    def editProfile(self, url, phone, first_name, biography, email, gender):
        return editProfile(self, url, phone, first_name, biography, email, gender)

    def getUsernameInfo(self, usernameId):
        return self.SendRequest('users/' + str(usernameId) + '/info/')

    def getSelfUsernameInfo(self):
        return self.getUsernameInfo(self.user_id)

    def getRecentActivity(self):
        activity = self.SendRequest('news/inbox/?')
        return activity

    def getFollowingRecentActivity(self):
        activity = self.SendRequest('news/?')
        return activity

    def getv2Inbox(self):
        inbox = self.SendRequest('direct_v2/inbox/?')
        return inbox

    def getUserTags(self, usernameId):
        tags = self.SendRequest('usertags/' + str(usernameId) +
                                '/feed/?rank_token=' + str(self.User.rank_token) + '&ranked_content=true&')
        return tags

    def getSelfUserTags(self):
        return self.getUserTags(self.User.user_id)

    def tagFeed(self, tag):
        userFeed = self.SendRequest(
            'feed/tag/' + str(tag) + '/?rank_token=' + str(self.User.rank_token) + '&ranked_content=true&')
        return userFeed

    def getMediaLikers(self, media_id):
        likers = self.SendRequest('media/' + str(media_id) + '/likers/?')
        return likers

    def getGeoMedia(self, usernameId):
        locations = self.SendRequest('maps/user/' + str(usernameId) + '/')
        return locations

    def getSelfGeoMedia(self):
        return self.getGeoMedia(self.User.user_id)

    def fbUserSearch(self, query):
        return fbUserSearch(self, query)

    def searchUsers(self, query):
        return searchUsers(self, query)

    def searchUsername(self, username):
        return searchUsername(self, username)

    def searchTags(self, query):
        return searchTags(self, query)

    def searchLocation(self, query):
        return searchLocation(self, query)

    def syncFromAdressBook(self, contacts):
        return self.SendRequest('address_book/link/?include=extra_display_name,thumbnails',
                                "contacts=" + json.dumps(contacts))

    def getTimeline(self):
        query = self.SendRequest(
            'feed/timeline/?rank_token=' + str(self.User.rank_token) + '&ranked_content=true&')
        return query

    def getUserFeed(self, usernameId, maxid='', minTimestamp=None):
        query = self.SendRequest(
            'feed/user/' + str(usernameId) + '/?max_id=' + str(maxid) + '&min_timestamp=' + str(minTimestamp) +
            '&rank_token=' + str(self.User.rank_token) + '&ranked_content=true')
        return query

    def getSelfUserFeed(self, maxid='', minTimestamp=None):
        return self.getUserFeed(self.User.user_id, maxid, minTimestamp)

    def getHashtagFeed(self, hashtagString, maxid=''):
        return self.SendRequest('feed/tag/' + hashtagString + '/?max_id=' + str(
            maxid) + '&rank_token=' + self.User.rank_token + '&ranked_content=true&')

    def getLocationFeed(self, locationId, maxid=''):
        return self.SendRequest('feed/location/' + str(locationId) + '/?max_id=' + str(
            maxid) + '&rank_token=' + self.User.rank_token + '&ranked_content=true&')

    def getPopularFeed(self):
        popularFeed = self.SendRequest(
            'feed/popular/?people_teaser_supported=1&rank_token=' + str(self.User.rank_token) + '&ranked_content=true&')
        return popularFeed

    def getUserFollowings(self, usernameId, maxid=''):
        return self.SendRequest('friendships/' + str(usernameId) + '/following/?max_id=' + str(maxid) +
                                '&ig_sig_key_version=' + config.SIG_KEY_VERSION + '&rank_token=' + self.User.rank_token)

    def getSelfUsersFollowing(self):
        return self.getUserFollowings(self.User.user_id)

    def getUserFollowers(self, usernameId, maxid=''):
        if maxid == '':
            return self.SendRequest('friendships/' + str(usernameId) + '/followers/?rank_token=' + self.User.rank_token)
        else:
            return self.SendRequest(
                'friendships/' + str(usernameId) + '/followers/?rank_token=' + self.User.rank_token + '&max_id=' + str(
                    maxid))

    def getSelfUserFollowers(self):
        return self.getUserFollowers(self.User.user_id)

    def like(self, mediaId):
        data = self.data_to_send_with({
            'media_id': mediaId
        })
        return self.SendRequest('media/' + str(mediaId) + '/like/', self.generateSignature(data))

    def unlike(self, mediaId):
        data = self.data_to_send_with({
            'media_id': mediaId
        })
        return self.SendRequest('media/' + str(mediaId) + '/unlike/', self.generateSignature(data))

    def getMediaComments(self, mediaId):
        return self.SendRequest('media/' + str(mediaId) + '/comments/?')

    def setNameAndPhone(self, name='', phone=''):
        return setNameAndPhone(self, name, phone)

    def getDirectShare(self):
        return self.SendRequest('direct_share/inbox/?')

    def follow(self, userId):
        data = self.data_to_send_with({
            'user_id': userId,
        })
        return self.SendRequest('friendships/create/' + str(userId) + '/', self.generateSignature(data))

    def unfollow(self, userId):
        data = self.data_to_send_with({
            'user_id': userId,
        })
        return self.SendRequest('friendships/destroy/' + str(userId) + '/', self.generateSignature(data))

    def block(self, userId):
        data = self.data_to_send_with({
            'user_id': userId,
        })
        return self.SendRequest('friendships/block/' + str(userId) + '/', self.generateSignature(data))

    def unblock(self, userId):
        data = self.data_to_send_with({
            'user_id': userId,
        })
        return self.SendRequest('friendships/unblock/' + str(userId) + '/', self.generateSignature(data))

    def userFriendship(self, userId):
        data = self.data_to_send_with({
            'user_id': userId,
        })
        return self.SendRequest('friendships/show/' + str(userId) + '/', self.generateSignature(data))

    def generateSignature(self, data):
        try:
            parsedData = urllib.parse.quote(data)
        except AttributeError:
            parsedData = urllib.quote(data)

        return 'ig_sig_key_version=' + config.SIG_KEY_VERSION + '&signed_body=' + hmac.new(
            config.IG_SIG_KEY.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest() + '.' + parsedData

    def getLikedMedia(self, maxid=''):
        return self.SendRequest('feed/liked/?max_id=' + str(maxid))

    def getTotalFollowers(self, usernameId):
        followers = []
        next_max_id = ''
        self.getUsernameInfo(usernameId)
        if "user" in self.LastJson:
            total_followers = self.LastJson["user"]['follower_count']
        else:
            return False
        with tqdm(total=total_followers, desc="Getting followers", leave=False) as pbar:
            while True:
                self.getUserFollowers(usernameId, next_max_id)
                temp = self.LastJson
                try:
                    pbar.update(len(temp["users"]))
                    for item in temp["users"]:
                        followers.append(item)
                    if len(temp["users"]) == 0 or len(followers) >= total_followers:
                        return followers[:total_followers]
                except:
                    return followers[:total_followers]
                if temp["big_list"] is False:
                    return followers[:total_followers]
                next_max_id = temp["next_max_id"]

    def getTotalFollowings(self, usernameId):
        following = []
        next_max_id = ''
        self.getUsernameInfo(usernameId)
        if "user" in self.LastJson:
            total_following = self.LastJson["user"]['following_count']
        else:
            return False
        with tqdm(total=total_following, desc="Getting following", leave=False) as pbar:
            while True:
                self.getUserFollowings(usernameId, next_max_id)
                temp = self.LastJson
                try:
                    pbar.update(len(temp["users"]))
                    for item in temp["users"]:
                        following.append(item)
                    if len(temp["users"]) == 0 or len(following) >= total_following:
                        return following[:total_following]
                except:
                    return following[:total_following]
                if temp["big_list"] is False:
                    return following[:total_following]
                next_max_id = temp["next_max_id"]

    def getTotalUserFeed(self, usernameId, minTimestamp=None):
        user_feed = []
        next_max_id = ''
        while 1:
            self.getUserFeed(usernameId, next_max_id, minTimestamp)
            temp = self.LastJson
            for item in temp["items"]:
                user_feed.append(item)
            if temp["more_available"] is False:
                return user_feed
            next_max_id = temp["next_max_id"]

    def getTotalSelfUserFeed(self, minTimestamp=None):
        return self.getTotalUserFeed(self.User.user_id, minTimestamp)

    def getTotalSelfFollowers(self):
        return self.getTotalFollowers(self.User.user_id)

    def getTotalSelfFollowings(self):
        return self.getTotalFollowings(self.User.user_id)

    def getTotalLikedMedia(self, scan_rate=1):
        next_id = ''
        liked_items = []
        for _ in range(0, scan_rate):
            temp = self.getLikedMedia(next_id)
            temp = self.LastJson
            next_id = temp["next_max_id"]
            for item in temp["items"]:
                liked_items.append(item)
        return liked_items
