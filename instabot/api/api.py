import requests
import json
import hashlib
import hmac
import urllib
import uuid
import sys
import logging
import time
from random import randint
from tqdm import tqdm
import os
from . import config
from .api_photo import configurePhoto
from .api_photo import uploadPhoto
from .api_photo import downloadPhoto

from .api_video import configureVideo
from .api_video import uploadVideo

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
from .api_db import  insert,getBotIp
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import socket

# The urllib library was split into other modules from Python 2 to Python 3
if sys.version_info.major == 3:
    import urllib.parse

class SourceAddressAdapter(HTTPAdapter):
    def __init__(self, source_address, **kwargs):
        self.source_address = source_address
        super(SourceAddressAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       source_address=self.source_address)

class API(object):
    def __init__(self):
        self.isLoggedIn = False
        self.LastResponse = None
        self.total_requests = 0

    def initLogging(self,id_campaign):
        filename = time.strftime("%d.%m.%Y") + ".log"

        if id_campaign==False:
            id_campaign="general"
            filename="instabot.log"
	    #this is not working atm
        #logs_folder = os.environ['INSTABOT_LOGS_PATH']
        logs_folder = "/home/instabot-log"
        campaign_folder = logs_folder + "/campaign/" + id_campaign


        log_path = campaign_folder + "/"+filename

        if not os.path.exists(campaign_folder):
            os.makedirs(campaign_folder)
        # handle logging
        self.logger = logging.getLogger('[instabot]')
        self.logger.setLevel(logging.DEBUG)
        logging.basicConfig(format='%(asctime)s %(message)s',
                            filename=log_path,
                            level=logging.INFO
                            )
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        #dirty hack -> disable the output to console
        if id_campaign!="general":
            self.logger.addHandler(ch)

    def setUser(self, username, password):
        self.username = username
        self.password = password
        self.uuid = self.generateUUID(True)

    def login(self, username=None, password=None, force=False, proxy=None):
        self.logger.info("Trying to login user %s with custom IP: %s" % (username, self.multiple_ip))
        if password is None:
            username, password = get_credentials(username=username)

        m = hashlib.md5()
        m.update(username.encode('utf-8') + password.encode('utf-8'))
        self.proxy = proxy
        self.device_id = self.generateDeviceId(m.hexdigest())
        self.setUser(username, password)

        if (not self.isLoggedIn or force):
            self.session = requests.Session()
            if self.proxy is not None:
                proxies = {
                    'http': 'http://' + self.proxy,
                    'https': 'http://' + self.proxy,
                }
                self.session.proxies.update(proxies)
            if self.multiple_ip is not None and self.multiple_ip is not False:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.bot_ip =  getBotIp(self, self.web_application_id_user, self.id_campaign)
                self.session.mount("http://", SourceAddressAdapter((str(self.bot_ip), 0)))
                self.session.mount("https://", SourceAddressAdapter((str(self.bot_ip), 0)))

            if (self.SendRequest('si/fetch_headers/?challenge_type=signup&guid=' + self.generateUUID(False),None, True)):

                data = {'phone_id': self.generateUUID(True),
                        '_csrftoken': self.LastResponse.cookies['csrftoken'],
                        'username': self.username,
                        'guid': self.uuid,
                        'device_id': self.device_id,
                        'password': self.password,
                        'login_attempt_count': '0'}

                if self.SendRequest('accounts/login/', self.generateSignature(json.dumps(data)), True):
                    self.isLoggedIn = True
                    self.user_id = self.LastJson["logged_in_user"]["pk"]
                    self.rank_token = "%s_%s" % (self.user_id, self.uuid)
                    self.token = self.LastResponse.cookies["csrftoken"]

                    self.logger.info("Login success as %s!" % self.username)
                    return True
                else:
                    self.logger.info("Login or password is incorrect.")
                    delete_credentials()
                    return False
            else:
                self.logger.info("Could not login user %s, going to exit !", username)
                return False

    def loadJson(self, value):
        try:
            r = json.loads(value)
            #self.logger.info("loadJson: Successfully loaded json !")
            return r
        except:
            self.logger.info("loadJson: Could not load json %s",value)
            return {}

    def logout(self):
        if not self.isLoggedIn:
            return True
        self.isLoggedIn = not self.SendRequest('accounts/logout/')
        return not self.isLoggedIn

    def SendRequest(self, endpoint, post=None, login=False):
        if (not self.isLoggedIn and not login):
            self.logger.critical("Not logged in.")
            raise Exception("Not logged in!")

        #self.logger.info("Requesting %s: ",config.API_URL + endpoint)
        self.session.headers.update({'Connection': 'close',
                                     'Accept': '*/*',
                                     'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                     'Cookie2': '$Version=1',
                                     'Accept-Language': 'en-US',
                                     'User-Agent': config.USER_AGENT})
        try:
            self.total_requests += 1
            if post is not None:  # POST
                response = self.session.post(
                    config.API_URL + endpoint, data=post, verify=True)
            else:  # GET
                response = self.session.get(
                    config.API_URL + endpoint,verify=True)
        except Exception as e:
            self.logger.warning(str(e))
            return False

        if response.status_code == 200:
            self.LastResponse = response
            self.LastJson = self.loadJson(response.text)
            return True
        else:
            details = None
            responseInfo = response.text
            self.logger.info("Request error url: %s: ", config.API_URL + endpoint)
						
            if response.status_code != 404:
                self.logger.warning("HTTP ERROR: STATUS %s , BODY: %s " % (str(response.status_code), response.text))
            else:#the original response  is too big when 404
                responseInfo="Page not found!"
                self.logger.warning("HTTP ERROR: STATUS %s, going to sleep 1 minute !" % (str(response.status_code)))
                sleep_minutes=1
                time.sleep(sleep_minutes * 60)


            if response.status_code == 400:
                responseObject = self.loadJson(response.text)
                if 'spam' in responseObject:
                    sleep_minutes = 10
                    self.logger.warning("BOT IS BLOCKED, going to sleep %s minutes" % sleep_minutes)
                    details="spam"
                    time.sleep(sleep_minutes * 60)
                else:
                    sleep_minutes=1
                    self.logger.warning("Request return 400 error. Going to sleep %s minutes" % sleep_minutes)
                    #don t sleep on login fail
                    if login==False:
                        time.sleep(sleep_minutes * 60)

            elif response.status_code == 429:
                sleep_minutes = 5
                details="That means too many requests"
                self.logger.warning("That means 'too many requests'. "
                                    "I'll go to sleep for %d minutes." % sleep_minutes)
                time.sleep(sleep_minutes * 60)

            currentOperation = self.currentOperation if hasattr(self, "currentOperation") else None

            insert("insert into instagram_log (id_user,log,operation,request,http_status,details,timestamp) values (%s,%s,%s,%s,%s,%s,now())",
                   self.web_application_id_user, responseInfo, currentOperation, config.API_URL + endpoint,str(response.status_code),details)

            # for debugging
            try:
                self.LastResponse = response
                self.LastJson = self.loadJson(response.text)
            except:
                pass
            return False

    def syncFeatures(self):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            'id': self.user_id,
            '_csrftoken': self.token,
            'experiments': config.EXPERIMENTS
        })
        return self.SendRequest('qe/sync/', self.generateSignature(data))

    def autoCompleteUserList(self):
        return self.SendRequest('friendships/autocomplete_user_list/')



    def getTimelineFeed(self, amount=20):
        self.logger.info("Trying to get %s items from timeline feed" % amount)

        user_feed = []
        next_max_id = None
        securityBreak=0

        while len(user_feed) < amount and securityBreak<50:

            if not next_max_id:
                self.SendRequest('feed/timeline/')
            else:
                self.SendRequest('feed/timeline/?max_id=' + str(next_max_id))

            temp = self.LastJson
            if "items" not in temp:  # maybe user is private, (we have not access to posts)
                return []

            for item in temp["items"]:
                if 'pk' in item.keys():
                    user_feed.append(item)

            if "next_max_id" not in temp:
                self.logger.info("Total received %s posts from timeline feed" % len(user_feed))
                return user_feed

            next_max_id = temp["next_max_id"]

            securityBreak = securityBreak+1
            self.logger.info("Iteration %s ,received %s items, total received %s" % (securityBreak, len(temp['items']), len(user_feed)))

            sleep_time = randint(1, 3)
            self.logger.info("Sleeping %s seconds" % sleep_time)
            time.sleep(sleep_time)


        self.logger.info("Total received %s posts from timeline feed" % len(user_feed))

        return user_feed

    def megaphoneLog(self):
        return self.SendRequest('megaphone/log/')

    def expose(self):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            'id': self.user_id,
            '_csrftoken': self.token,
            'experiment': 'ig_android_profile_contextual_feed'
        })
        return self.SendRequest('qe/expose/', self.generateSignature(data))

    def uploadPhoto(self, photo, caption=None, upload_id=None):
        return uploadPhoto(self, photo, caption, upload_id)

    def downloadPhoto(self, media_id, filename, media=False, path='photos/'):
        return downloadPhoto(self, media_id, filename, media, path)

    def configurePhoto(self, upload_id, photo, caption=''):
        return configurePhoto(self, upload_id, photo, caption)

    def uploadVideo(self, photo, caption=None, upload_id=None):
        return uploadVideo(self, photo, caption, upload_id)

    def configureVideo(self, upload_id, video, thumbnail, caption=''):
        return configureVideo(self, upload_id, video, thumbnail, caption)

    def editMedia(self, mediaId, captionText=''):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            '_csrftoken': self.token,
            'caption_text': captionText
        })
        return self.SendRequest('media/' + str(mediaId) + '/edit_media/', self.generateSignature(data))

    def removeSelftag(self, mediaId):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            '_csrftoken': self.token
        })
        return self.SendRequest('media/' + str(mediaId) + '/remove/', self.generateSignature(data))

    def mediaInfo(self, mediaId):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            '_csrftoken': self.token,
            'media_id': mediaId
        })
        return self.SendRequest('media/' + str(mediaId) + '/info/', self.generateSignature(data))

    def archiveMedia(self, media, undo=False):
        action = 'only_me' if not undo else 'undo_only_me'
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            '_csrftoken': self.token,
            'media_id': media['id']
        })
        return self.SendRequest('media/' + str(media['id']) + '/' + str(action) + '/?media_type=' +
                                str(media['media_type']), self.generateSignature(data))

    def deleteMedia(self, mediaId):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            '_csrftoken': self.token,
            'media_id': mediaId
        })
        return self.SendRequest('media/' + str(mediaId) + '/delete/', self.generateSignature(data))

    def changePassword(self, newPassword):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            '_csrftoken': self.token,
            'old_password': self.password,
            'new_password1': newPassword,
            'new_password2': newPassword
        })
        return self.SendRequest('accounts/change_password/', self.generateSignature(data))

    def explore(self):
        return self.SendRequest('discover/explore/')

    def comment(self, mediaId, commentText):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            '_csrftoken': self.token,
            'comment_text': commentText
        })
        return self.SendRequest('media/' + str(mediaId) + '/comment/', self.generateSignature(data))

    def deleteComment(self, mediaId, commentId):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            '_csrftoken': self.token
        })
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
                                '/feed/?rank_token=' + str(self.rank_token) + '&ranked_content=true&')
        return tags

    def getSelfUserTags(self):
        return self.getUserTags(self.user_id)

    def tagFeed(self, tag):
        userFeed = self.SendRequest(
            'feed/tag/' + str(tag) + '/?rank_token=' + str(self.rank_token) + '&ranked_content=true&')
        return userFeed

    def getMediaLikers(self, media_id):
        likers = self.SendRequest('media/' + str(media_id) + '/likers/?')
        return likers

    def getGeoMedia(self, usernameId):
        locations = self.SendRequest('maps/user/' + str(usernameId) + '/')
        return locations

    def getSelfGeoMedia(self):
        return self.getGeoMedia(self.user_id)

    def fbUserSearch(self, query):
        return fbUserSearch(self, query)

    def searchUsers(self, query):
        return searchUsers(self, query)

    def searchUsername(self, username):
        return searchUsername(self, username)

    def searchTags(self, query):
        return searchTags(self, query)

    def searchLocation(self, query='', lat=None, lng=None):
        return searchLocation(self, query, lat, lng)

    def syncFromAdressBook(self, contacts):
        return self.SendRequest('address_book/link/?include=extra_display_name,thumbnails',
                                "contacts=" + json.dumps(contacts))

    def getTimeline(self):
        query = self.SendRequest(
            'feed/timeline/?rank_token=' + str(self.rank_token) + '&ranked_content=true&')
        return query

    def getArchiveFeed(self):
        query = self.SendRequest(
            'feed/only_me_feed/?rank_token=' + str(self.rank_token) + '&ranked_content=true&')
        return query

    def getUserFeed(self, usernameId, maxid='', minTimestamp=None):

        query = self.SendRequest(
            'feed/user/' + str(usernameId) + '/?max_id=' + str(maxid) + '&min_timestamp=' + str(minTimestamp) +
            '&rank_token=' + str(self.rank_token) + '&ranked_content=true')
        
        items=0
        
        if 'items' in self.LastJson:
           items=len(self.LastJson['items'])
        
        self.logger.info("api: Received %s items from user %s feed" %(items, usernameId))
        
        sleep_time = randint(1, 3)
        self.logger.info("api: Sleeping %s seconds" % sleep_time)
        time.sleep(sleep_time)
            
        return query

    def getSelfUserFeed(self, maxid='', minTimestamp=None):
        return self.getUserFeed(self.user_id, maxid, minTimestamp)

    def getHashtagFeed(self, hashtagString, amount=50):
        self.logger.info("Trying to get %s medias with hashtag %s" % (amount, hashtagString))

        feed = []
        next_max_id = None
        securityBreak = 0

        while len(feed)<amount and securityBreak<50:
            if not next_max_id:
                self.SendRequest('feed/tag/' + hashtagString)
            else:
                self.SendRequest('feed/tag/' + hashtagString + '/?max_id='+str(next_max_id))

            temp = self.LastJson
						
			#the result is damaged
            if "items" not in temp:
                self.logger.info("Total Received %s items with hashtag %s" % (len(feed), hashtagString))
                return feed

            for item in temp["items"]:
                if 'pk' in item.keys():
                    feed.append(item)

            if "next_max_id" not in temp:
                self.logger.info("Total Received %s items with hashtag %s" % (len(feed), hashtagString))
                return feed

            next_max_id = temp["next_max_id"]

            self.logger.info("Iteration %s ,received %s items, total received %s" % (securityBreak, len(temp['items']), len(feed)))
            securityBreak = securityBreak + 1
            sleep_time = randint(1, 3)
            self.logger.info("Sleeping %s seconds" % sleep_time)
            time.sleep(sleep_time)


        self.logger.info("Total Received %s items with hashtag %s" % (len(feed),hashtagString))
        return feed

    def getLocationFeed(self, locationId, amount):
        self.logger.info("Getting %s medias from location: %s" % (amount,locationId))

        feed = []
        next_max_id = None
        security_check=0

        while len(feed)<amount and security_check<100:

            if not next_max_id:
                self.SendRequest('feed/location/' + str(locationId))
            else:
                self.SendRequest('feed/location/' + str(locationId) + '/?max_id=' + str(next_max_id))

            temp = self.LastJson

            #the result is damaged
            if "items" not in temp: #if no items
                self.logger.info("Retrieved %s medias from location %s" % (len(feed), locationId))
                return feed

            for item in temp["items"]:
                feed.append(item)

            if "next_max_id" in temp:
                next_max_id = temp["next_max_id"]
            else:
                self.logger.info('Next max id is empty, going to return !')
                self.logger.info("Retrieved %s medias from location %s" % (len(feed),locationId))
                return feed

            security_check +=1

            sleep_time = randint(1, 3)
            self.logger.info("Iteration %s ,received %s items, total received %s" % (security_check, len(temp['items']), len(feed)))

            self.logger.info("Sleeping %s seconds" % sleep_time)
            time.sleep(sleep_time)

        self.logger.info("Retrieved %s medias from location %s" % (len(feed),locationId))
        return feed


    def getPopularFeed(self):
        popularFeed = self.SendRequest(
            'feed/popular/?people_teaser_supported=1&rank_token=' + str(self.rank_token) + '&ranked_content=true&')
        return popularFeed

    def getUserFollowings(self, usernameId, maxid=''):
        return self.SendRequest('friendships/' + str(usernameId) + '/following/?max_id=' + str(maxid) +
                                '&ig_sig_key_version=' + config.SIG_KEY_VERSION + '&rank_token=' + self.rank_token)

    def getSelfUsersFollowing(self):
        return self.getUserFollowings(self.user_id)

 
    def getSelfUserFollowers(self):
        return self.getUserFollowers(self.user_id)

    def like(self, mediaId):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            '_csrftoken': self.token,
            'media_id': mediaId
        })
        return self.SendRequest('media/' + str(mediaId) + '/like/', self.generateSignature(data))

    def unlike(self, mediaId):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            '_csrftoken': self.token,
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
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            'user_id': userId,
            '_csrftoken': self.token
        })
        return self.SendRequest('friendships/create/' + str(userId) + '/', self.generateSignature(data))

    def unfollow(self, userId):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            'user_id': userId,
            '_csrftoken': self.token
        })
        return self.SendRequest('friendships/destroy/' + str(userId) + '/', self.generateSignature(data))

    def block(self, userId):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            'user_id': userId,
            '_csrftoken': self.token
        })
        return self.SendRequest('friendships/block/' + str(userId) + '/', self.generateSignature(data))

    def unblock(self, userId):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            'user_id': userId,
            '_csrftoken': self.token
        })
        return self.SendRequest('friendships/unblock/' + str(userId) + '/', self.generateSignature(data))

    def userFriendship(self, userId):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            'user_id': userId,
            '_csrftoken': self.token
        })
        return self.SendRequest('friendships/show/' + str(userId) + '/', self.generateSignature(data))

    def generateSignature(self, data):
        try:
            parsedData = urllib.parse.quote(data)
        except AttributeError:
            parsedData = urllib.quote(data)

        return 'ig_sig_key_version=' + config.SIG_KEY_VERSION + '&signed_body=' + hmac.new(
            config.IG_SIG_KEY.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest() + '.' + parsedData

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

    def getLikedMedia(self, maxid=''):
        return self.SendRequest('feed/liked/?max_id=' + str(maxid))

    def getUserFollowers(self, usernameId, amount=50, next_max_id=None):
        self.logger.info("Trying to get %s followers  of %s This might take a while." % (amount,usernameId))
        self.logger.info("Next max id is: %s",next_max_id)
        followers = []
        securityBreak=0
        result={}
        previous_next_max_id=next_max_id
        while len(followers) < amount and securityBreak < 100:
   
            if next_max_id == '' or next_max_id==None:
              self.SendRequest('friendships/' + str(usernameId) + '/followers')
            else:
              self.SendRequest('friendships/' + str(usernameId) + '/followers/?max_id=' + str(next_max_id))
          
            temp = self.LastJson

            # the result is damaged
            if "users" not in temp:  # if no items
                self.logger.info("End of the line: Total received %s followers of user %s" % (len(followers), usernameId))
                result['followers'] = followers
                result['next_max_id'] = None
                result['previous_next_max_id'] = previous_next_max_id
                return result

            for item in temp["users"]:
                followers.append(item)

            securityBreak = securityBreak + 1
            self.logger.info("Iteration %s ,received %s items, total received %s followers" % (securityBreak, len(temp['users']), len(followers)))

            if "next_max_id" not in temp:
                self.logger.info("End of the line: Total received %s followers of user %s" % (len(followers), usernameId))
                result['followers'] = followers
                result['next_max_id']=None
                result['previous_next_max_id']=previous_next_max_id
                return result

            next_max_id = temp["next_max_id"]
            previous_next_max_id = next_max_id


            sleep_time = randint(5, 10)
            self.logger.info("Sleeping %s seconds" % sleep_time)
            time.sleep(sleep_time)

        self.logger.info("Total received %s followers of user %s" % (len(followers), usernameId))

        result['followers'] = followers
        result['next_max_id'] = next_max_id
        result['previous_next_max_id'] = previous_next_max_id
        return result

    def getTotalFollowings(self, usernameId, amount=None):
        sleep_track = 0
        following = []
        next_max_id = ''
        self.getUsernameInfo(usernameId)
        if "user" in self.LastJson:
            if amount:
                total_following = amount
            else:
                total_following = self.LastJson["user"]['following_count']
            if total_following > 200000:
                print("Consider temporarily saving the result of this big operation. This will take a while.\n")
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
                        sleep_track += 1
                        if sleep_track >= 20000:
                            sleep_time = randint(120, 180)
                            print("\nWaiting %.2f min. due to too many requests." % float(sleep_time / 60))
                            time.sleep(sleep_time)
                            sleep_track = 0
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
            if "items" not in temp:  # maybe user is private, (we have not access to posts)
                return []
            for item in temp["items"]:
                user_feed.append(item)
            if "more_available" not in temp or temp["more_available"] is False:
                return user_feed
            next_max_id = temp["next_max_id"]

    #this gives all medias posted by the logged user
    def getTotalSelfUserFeed(self, minTimestamp=None):
        return self.getTotalUserFeed(self.user_id, minTimestamp)

    def getTotalSelfFollowers(self):
        return self.getTotalFollowers(self.user_id)

    def getTotalSelfFollowings(self):
        return self.getTotalFollowings(self.user_id)

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
