import requests
import random
import json
import hashlib
import hmac
import urllib
import uuid
import sys

#The urllib library was split into other modules from Python 2 to Python 3
if sys.version_info.major == 3:
    import urllib.parse

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

class API(object):
    def __init__(self):
        self.isLoggedIn = False
        self.LastResponse = None

    def setUser(self, username, password):
        self.username = username
        self.password = password
        self.uuid = self.generateUUID(True)

    def login(self, username = None, password = None, force = False):
        if username is None or password is None:
            username, password = get_credentials()

        m = hashlib.md5()
        m.update(username.encode('utf-8') + password.encode('utf-8'))
        self.device_id = self.generateDeviceId(m.hexdigest())
        self.setUser(username, password)

        if (not self.isLoggedIn or force):
            self.session = requests.Session()
            # if you need proxy make something like this:
            # self.session.proxies = {"https" : "http://proxyip:proxyport"}
            if (self.SendRequest('si/fetch_headers/?challenge_type=signup&guid=' + self.generateUUID(False), None, True)):

                data = {'phone_id'   : self.generateUUID(True),
                        '_csrftoken' : self.LastResponse.cookies['csrftoken'],
                        'username'   : self.username,
                        'guid'       : self.uuid,
                        'device_id'  : self.device_id,
                        'password'   : self.password,
                        'login_attempt_count' : '0'}

                if self.SendRequest('accounts/login/', self.generateSignature(json.dumps(data)), True):
                    self.isLoggedIn = True
                    self.username_id = self.LastJson["logged_in_user"]["pk"]
                    self.rank_token = "%s_%s" % (self.username_id, self.uuid)
                    self.token = self.LastResponse.cookies["csrftoken"]

                    # self.syncFeatures()
                    # self.autoCompleteUserList()
                    # self.getTimelineFeed()
                    # self.getv2Inbox()
                    # self.getRecentActivity()
                    print ("Login success!\n")
                    return True
                else:
                    print ("Login or password is incorrect.")
                    delete_credentials()
                    exit()

    def logout(self):
        if not self.isLoggedIn:
            return True
        return self.SendRequest('accounts/logout/')

    def SendRequest(self, endpoint, post = None, login = False):
        if (not self.isLoggedIn and not login):
            raise Exception("Not logged in!\n")

        self.session.headers.update({'Connection' : 'close',
                                'Accept' : '*/*',
                                'Content-type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                                'Cookie2' : '$Version=1',
                                'Accept-Language' : 'en-US',
                                'User-Agent' : config.USER_AGENT})

        if (post != None): # POST
            response = self.session.post(config.API_URL + endpoint, data=post) # , verify=False
        else: # GET
            response = self.session.get(config.API_URL + endpoint) # , verify=False

        if response.status_code == 200:
            self.LastResponse = response
            self.LastJson = json.loads(response.text)
            return True
        else:
            print ("Request return " + str(response.status_code) + " error!")
            # for debugging
            try:
                self.LastResponse = response
                self.LastJson = json.loads(response.text)
            except:
                pass
            return False

    def syncFeatures(self):
        data = json.dumps({
        '_uuid'         : self.uuid,
        '_uid'          : self.username_id,
        'id'            : self.username_id,
        '_csrftoken'    : self.token,
        'experiments'   : config.EXPERIMENTS
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
        data = json.dumps({
        '_uuid'        : self.uuid,
        '_uid'         : self.username_id,
        'id'           : self.username_id,
        '_csrftoken'   : self.token,
        'experiment'   : 'ig_android_profile_contextual_feed'
        })
        return self.SendRequest('qe/expose/', self.generateSignature(data))

    def uploadPhoto(self, photo, caption = None, upload_id = None):
        return uploadPhoto(self, photo, caption, upload_id)

    def configurePhoto(self, upload_id, photo, caption = ''):
        return configurePhoto(self, upload_id, photo, caption)

    def editMedia(self, mediaId, captionText = ''):
        data = json.dumps({
        '_uuid'        : self.uuid,
        '_uid'         : self.username_id,
        '_csrftoken'   : self.token,
        'caption_text' : captionText
        })
        return self.SendRequest('media/'+ str(mediaId) +'/edit_media/', self.generateSignature(data))

    def removeSelftag(self, mediaId):
        data = json.dumps({
        '_uuid'        : self.uuid,
        '_uid'         : self.username_id,
        '_csrftoken'   : self.token
        })
        return self.SendRequest('media/'+ str(mediaId) +'/remove/', self.generateSignature(data))

    def mediaInfo(self, mediaId):
        data = json.dumps({
        '_uuid'        : self.uuid,
        '_uid'         : self.username_id,
        '_csrftoken'   : self.token,
        'media_id'     : mediaId
        })
        return self.SendRequest('media/'+ str(mediaId) +'/info/', self.generateSignature(data))

    def deleteMedia(self, mediaId):
        data = json.dumps({
        '_uuid'        : self.uuid,
        '_uid'         : self.username_id,
        '_csrftoken'   : self.token,
        'media_id'     : mediaId
        })
        return self.SendRequest('media/'+ str(mediaId) +'/delete/', self.generateSignature(data))

    def changePassword(self, newPassword):
        data = json.dumps({
        '_uuid'        : self.uuid,
        '_uid'         : self.username_id,
        '_csrftoken'   : self.token,
        'old_password'  : self.password,
        'new_password1' : newPassword,
        'new_password2' : newPassword
        })
        return self.SendRequest('accounts/change_password/', self.generateSignature(data))

    def explore(self):
        return self.SendRequest('discover/explore/')

    def comment(self, mediaId, commentText):
        data = json.dumps({
        '_uuid'        : self.uuid,
        '_uid'         : self.username_id,
        '_csrftoken'   : self.token,
        'comment_text' : commentText
        })
        return self.SendRequest('media/'+ str(mediaId) +'/comment/', self.generateSignature(data))

    def deleteComment(self, mediaId, commentId):
        data = json.dumps({
        '_uuid'        : self.uuid,
        '_uid'         : self.username_id,
        '_csrftoken'   : self.token
        })
        return self.SendRequest('media/'+ str(mediaId) +'/comment/'+ str(commentId) +'/delete/', self.generateSignature(data))

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
        return self.SendRequest('users/'+ str(usernameId) +'/info/')

    def getSelfUsernameInfo(self):
        return self.getUsernameInfo(self.username_id)

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
        tags = self.SendRequest('usertags/'+ str(usernameId) +'/feed/?rank_token='+ str(self.rank_token) +'&ranked_content=true&')
        return tags

    def getSelfUserTags(self):
        return self.getUserTags(self.username_id)

    def tagFeed(self, tag):
        userFeed = self.SendRequest('feed/tag/'+ str(tag) +'/?rank_token=' + str(self.rank_token) + '&ranked_content=true&')
        return userFeed

    def getMediaLikers(self, mediaId):
        likers = self.SendRequest('media/'+ str(mediaId) +'/likers/?')
        return likers

    def getGeoMedia(self, usernameId):
        locations = self.SendRequest('maps/user/'+ str(usernameId) +'/')
        return locations

    def getSelfGeoMedia(self):
        return self.getGeoMedia(self.username_id)

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
        return self.SendRequest('address_book/link/?include=extra_display_name,thumbnails', "contacts=" + json.dumps(contacts))

    def getTimeline(self):
        query = self.SendRequest('feed/timeline/?rank_token='+ str(self.rank_token) +'&ranked_content=true&')
        return query

    def getUserFeed(self, usernameId, maxid = '', minTimestamp = None):
        query = self.SendRequest('feed/user/' + str(usernameId) + '/?max_id=' + str(maxid) + '&min_timestamp=' + str(minTimestamp)
            + '&rank_token='+ str(self.rank_token) +'&ranked_content=true')
        return query

    def getSelfUserFeed(self, maxid = '', minTimestamp = None):
        return self.getUserFeed(self.username_id, maxid, minTimestamp)

    def getHashtagFeed(self, hashtagString, maxid = ''):
        return self.SendRequest('feed/tag/'+hashtagString+'/?max_id='+str(maxid)+'&rank_token='+self.rank_token+'&ranked_content=true&')

    def getLocationFeed(self, locationId, maxid = ''):
        return self.SendRequest('feed/location/'+str(locationId)+'/?max_id='+maxid+'&rank_token='+self.rank_token+'&ranked_content=true&')

    def getPopularFeed(self):
        popularFeed = self.SendRequest('feed/popular/?people_teaser_supported=1&rank_token='+ str(self.rank_token) +'&ranked_content=true&')
        return popularFeed

    def getUserFollowings(self, usernameId, maxid = ''):
        return self.SendRequest('friendships/'+ str(usernameId) +'/following/?max_id='+ str(maxid)
            +'&ig_sig_key_version='+ config.SIG_KEY_VERSION +'&rank_token='+ self.rank_token)

    def getSelfUsersFollowing(self):
        return self.getUserFollowings(self.username_id)

    def getUserFollowers(self, usernameId, maxid = ''):
        if maxid == '':
            return self.SendRequest('friendships/'+ str(usernameId) +'/followers/?rank_token='+ self.rank_token)
        else:
            return self.SendRequest('friendships/'+ str(usernameId) +'/followers/?rank_token='+ self.rank_token + '&max_id='+ str(maxid))

    def getSelfUserFollowers(self):
        return self.getUserFollowers(self.username_id)

    def like(self, mediaId):
        data = json.dumps({
        '_uuid'         : self.uuid,
        '_uid'          : self.username_id,
        '_csrftoken'    : self.token,
        'media_id'      : mediaId
        })
        return self.SendRequest('media/'+ str(mediaId) +'/like/', self.generateSignature(data))

    def unlike(self, mediaId):
        data = json.dumps({
        '_uuid'         : self.uuid,
        '_uid'          : self.username_id,
        '_csrftoken'    : self.token,
        'media_id'      : mediaId
        })
        return self.SendRequest('media/'+ str(mediaId) +'/unlike/', self.generateSignature(data))

    def getMediaComments(self, mediaId):
        return self.SendRequest('media/'+ mediaId +'/comments/?')

    def setNameAndPhone(self, name = '', phone = ''):
        return setNameAndPhone(self, name, phone)

    def getDirectShare(self):
        return self.SendRequest('direct_share/inbox/?')

    def follow(self, userId):
        data = json.dumps({
        '_uuid'         : self.uuid,
        '_uid'          : self.username_id,
        'user_id'       : userId,
        '_csrftoken'    : self.token
        })
        return self.SendRequest('friendships/create/'+ str(userId) +'/', self.generateSignature(data))

    def unfollow(self, userId):
        data = json.dumps({
        '_uuid'         : self.uuid,
        '_uid'          : self.username_id,
        'user_id'       : userId,
        '_csrftoken'    : self.token
        })
        return self.SendRequest('friendships/destroy/'+ str(userId) +'/', self.generateSignature(data))

    def block(self, userId):
        data = json.dumps({
        '_uuid'         : self.uuid,
        '_uid'          : self.username_id,
        'user_id'       : userId,
        '_csrftoken'    : self.token
        })
        return self.SendRequest('friendships/block/'+ str(userId) +'/', self.generateSignature(data))

    def unblock(self, userId):
        data = json.dumps({
        '_uuid'         : self.uuid,
        '_uid'          : self.username_id,
        'user_id'       : userId,
        '_csrftoken'    : self.token
        })
        return self.SendRequest('friendships/unblock/'+ str(userId) +'/', self.generateSignature(data))

    def userFriendship(self, userId):
        data = json.dumps({
        '_uuid'         : self.uuid,
        '_uid'          : self.username_id,
        'user_id'       : userId,
        '_csrftoken'    : self.token
        })
        return self.SendRequest('friendships/show/'+ str(userId) +'/', self.generateSignature(data))

    def generateSignature(self, data):
        try:
            parsedData = urllib.parse.quote(data)
        except AttributeError:
            parsedData = urllib.quote(data)

        return 'ig_sig_key_version=' + config.SIG_KEY_VERSION + '&signed_body=' + hmac.new(config.IG_SIG_KEY.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest() + '.' + parsedData

    def generateDeviceId(self, seed):
        volatile_seed = "12345"
        m = hashlib.md5()
        m.update(seed.encode('utf-8') + volatile_seed.encode('utf-8'))
        return 'android-' + m.hexdigest()[:16]

    def generateUUID(self, uuid_type):
        generated_uuid = str(uuid.uuid4())
        if (uuid_type):
            return generated_uuid
        else:
            return generated_uuid.replace('-', '')

    def getLikedMedia(self,maxid=''):
        return self.SendRequest('feed/liked/?max_id='+str(maxid))

    def getTotalFollowers(self,usernameId):
        followers = []
        next_max_id = ''
        while 1:
            self.getUserFollowers(usernameId,next_max_id)
            temp = self.LastJson

            for item in temp["users"]:
                followers.append(item)

            if temp["big_list"] == False:
                return followers
            next_max_id = temp["next_max_id"]

    def getTotalFollowings(self,usernameId):
        followers = []
        next_max_id = ''
        while 1:
            self.getUserFollowings(usernameId,next_max_id)
            temp = self.LastJson

            for item in temp["users"]:
                followers.append(item)

            if temp["big_list"] == False:
                return followers
            next_max_id = temp["next_max_id"]

    def getTotalUserFeed(self, usernameId, minTimestamp = None):
        user_feed = []
        next_max_id = ''
        while 1:
            self.getUserFeed(usernameId, next_max_id, minTimestamp)
            temp = self.LastJson
            for item in temp["items"]:
                user_feed.append(item)
            if temp["more_available"] == False:
                return user_feed
            next_max_id = temp["next_max_id"]

    def getTotalSelfUserFeed(self, minTimestamp = None):
        return self.getTotalUserFeed(self.username_id, minTimestamp)

    def getTotalSelfFollowers(self):
        return self.getTotalFollowers(self.username_id)

    def getTotalSelfFollowings(self):
        return self.getTotalFollowings(self.username_id)

    def getTotalLikedMedia(self, scan_rate = 1):
        next_id = ''
        liked_items = []
        for _ in range(0,scan_rate):
            temp = self.getLikedMedia(next_id)
            temp = self.LastJson
            next_id = temp["next_max_id"]
            for item in temp["items"]:
                liked_items.append(item)
        return liked_items

# TODOs:

    def changeProfilePicture(self, photo):
        # TODO Instagram.php 705-775
        return False

    def direct_share(self, media_id, recipients, text = None):
        # TODO Instagram.php 420-490
        return False

    def buildBody(bodies, boundary):
        # TODO Instagram.php 1620-1645
        return False

    def backup(self):
        # TODO Instagram.php 1470-1485
        return False
