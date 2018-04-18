import hashlib
import hmac
import json
import logging
import sys
import time
import urllib
import uuid
from random import randint

import requests
from tqdm import tqdm

from . import config
from .api_photo import configure_photo, download_photo, upload_photo
from .api_profile import (edit_profile, get_profile_data, remove_profile_picture,
                          set_name_and_phone, set_private_account, set_public_account)
from .api_search import (fb_user_search, search_location, search_tags,
                         search_username, search_users)
from .api_video import configure_video, download_video, upload_video
from .prepare import delete_credentials, get_credentials

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

# The urllib library was split into other modules from Python 2 to Python 3
if sys.version_info > (3,):
    import urllib.parse


class API(object):
    def __init__(self):
        self.is_logged_in = False
        self.last_response = None
        self.total_requests = 0

        # handle logging
        self.logger = logging.getLogger('[instabot_{}]'.format(id(self)))

        fh = logging.FileHandler(filename='instabot.log')
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s %(message)s')
        fh.setFormatter(formatter)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        self.logger.setLevel(logging.DEBUG)

    def set_user(self, username, password):
        self.username = username
        self.password = password
        self.uuid = self.generate_UUID(True)

    def login(self, username=None, password=None, force=False, proxy=None):
        if password is None:
            username, password = get_credentials(username=username)

        m = hashlib.md5()
        m.update(username.encode('utf-8') + password.encode('utf-8'))
        self.proxy = proxy
        self.device_id = self.generate_device_id(m.hexdigest())
        self.set_user(username, password)

        if (not self.is_logged_in or force):
            self.session = requests.Session()
            if self.proxy is not None:
                parsed = urlparse(self.proxy)
                scheme = 'http://' if not parsed.scheme else ''
                proxies = {
                    'http': scheme + self.proxy,
                    'https': scheme + self.proxy,
                }
                self.session.proxies.update(proxies)
            if (
                    self.send_request('si/fetch_headers/?challenge_type=signup&guid=' + self.generate_UUID(False),
                                     None, True)):

                data = {'phone_id': self.generate_UUID(True),
                        '_csrftoken': self.last_response.cookies['csrftoken'],
                        'username': self.username,
                        'guid': self.uuid,
                        'device_id': self.device_id,
                        'password': self.password,
                        'login_attempt_count': '0'}

                if self.send_request('accounts/login/', self.generate_signature(json.dumps(data)), True):
                    self.is_logged_in = True
                    self.user_id = self.last_json["logged_in_user"]["pk"]
                    self.rank_token = "%s_%s" % (self.user_id, self.uuid)
                    self.token = self.last_response.cookies["csrftoken"]

                    self.logger.info("Login success as %s!", self.username)
                    return True
                else:
                    self.logger.info("Login or password is incorrect.")
                    delete_credentials()
                    return False

    def logout(self):
        if not self.is_logged_in:
            return True
        self.is_logged_in = not self.send_request('accounts/logout/')
        return not self.is_logged_in

    def send_request(self, endpoint, post=None, login=False):
        if (not self.is_logged_in and not login):
            self.logger.critical("Not logged in.")
            raise Exception("Not logged in!")

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
                    config.API_URL + endpoint, data=post)
            else:  # GET
                response = self.session.get(
                    config.API_URL + endpoint)
        except Exception as e:
            self.logger.warning(str(e))
            return False

        if response.status_code == 200:
            self.last_response = response
            self.last_json = json.loads(response.text)
            return True
        else:
            self.logger.error("Request return %s error!", str(response.status_code))
            if response.status_code == 429:
                sleep_minutes = 5
                self.logger.warning("That means 'too many requests'. "
                                    "I'll go to sleep for %d minutes.", sleep_minutes)
                time.sleep(sleep_minutes * 60)
            elif response.status_code == 400:
                response_data = json.loads(response.text)
                self.logger.info("Instagram error message: %s", response_data.get('message'))
                if response_data.get('error_type'):
                    self.logger.info('Error type: %s', response_data.get('error_type'))

            # for debugging
            try:
                self.last_response = response
                self.last_json = json.loads(response.text)
            except Exception:
                pass
            return False

    def sync_features(self):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            'id': self.user_id,
            '_csrftoken': self.token,
            'experiments': config.EXPERIMENTS
        })
        return self.send_request('qe/sync/', self.generate_signature(data))

    def auto_complete_user_list(self):
        return self.send_request('friendships/autocomplete_user_list/')

    def get_timeline_feed(self):
        """ Returns 8 medias from timeline feed of logged user """
        return self.send_request('feed/timeline/')

    def get_megaphone_log(self):
        return self.send_request('megaphone/log/')

    def expose(self):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            'id': self.user_id,
            '_csrftoken': self.token,
            'experiment': 'ig_android_profile_contextual_feed'
        })
        return self.send_request('qe/expose/', self.generate_signature(data))

    def upload_photo(self, photo, caption=None, upload_id=None):
        return upload_photo(self, photo, caption, upload_id)

    def download_photo(self, media_id, filename, media=False, path='photos/'):
        return download_photo(self, media_id, filename, media, path)

    def configure_photo(self, upload_id, photo, caption=''):
        return configure_photo(self, upload_id, photo, caption)

    def upload_video(self, photo, caption=None, upload_id=None):
        return upload_video(self, photo, caption, upload_id)

    def download_video(self, media_id, filename, media=False, path='video/'):
        return download_video(self, media_id, filename, media, path)

    def configure_video(self, upload_id, video, thumbnail, caption=''):
        return configure_video(self, upload_id, video, thumbnail, caption)

    def edit_media(self, media_id, captionText=''):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            '_csrftoken': self.token,
            'caption_text': captionText
        })
        return self.send_request('media/' + str(media_id) + '/edit_media/', self.generate_signature(data))

    def remove_self_tag(self, media_id):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            '_csrftoken': self.token
        })
        return self.send_request('media/' + str(media_id) + '/remove/', self.generate_signature(data))

    def media_info(self, media_id):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            '_csrftoken': self.token,
            'media_id': media_id
        })
        return self.send_request('media/' + str(media_id) + '/info/', self.generate_signature(data))

    def archive_media(self, media, undo=False):
        action = 'only_me' if not undo else 'undo_only_me'
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            '_csrftoken': self.token,
            'media_id': media['id']
        })
        url = 'media/{media_id}/{action}/?media_type={media_type}'.format(
            media_id=media['id'],
            action=action,
            media_type=media['media_type']
        )
        return self.send_request(url, self.generate_signature(data))

    def delete_media(self, media):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            '_csrftoken': self.token,
            'media_id': media.get('id')
        })
        return self.send_request('media/' + str(media.get('id')) + '/delete/', self.generate_signature(data))

    def change_password(self, newPassword):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            '_csrftoken': self.token,
            'old_password': self.password,
            'new_password1': newPassword,
            'new_password2': newPassword
        })
        return self.send_request('accounts/change_password/', self.generate_signature(data))

    def explore(self):
        return self.send_request('discover/explore/')

    def comment(self, media_id, comment_text):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            '_csrftoken': self.token,
            'comment_text': comment_text
        })
        return self.send_request('media/' + str(media_id) + '/comment/', self.generate_signature(data))

    def delete_comment(self, media_id, comment_id):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            '_csrftoken': self.token
        })
        return self.send_request('media/' + str(media_id) + '/comment/' + str(comment_id) + '/delete/',
                                self.generate_signature(data))

    def remove_profile_picture(self):
        return remove_profile_picture(self)

    def set_private_account(self):
        return set_private_account(self)

    def set_public_account(self):
        return set_public_account(self)

    def get_profile_data(self):
        return get_profile_data(self)

    def edit_profile(self, url, phone, first_name, biography, email, gender):
        return edit_profile(self, url, phone, first_name, biography, email, gender)

    def get_username_info(self, username_id):
        return self.send_request('users/' + str(username_id) + '/info/')

    def get_self_username_info(self):
        return self.get_username_info(self.user_id)

    def get_recent_activity(self):
        activity = self.send_request('news/inbox/?')
        return activity

    def get_following_recent_activity(self):
        activity = self.send_request('news/?')
        return activity

    def getv2Inbox(self):
        inbox = self.send_request('direct_v2/inbox/?')
        return inbox

    def get_user_tags(self, username_id):
        url = 'usertags/{username_id}/feed/?rank_token={rank_token}&ranked_content=true&'.format(
            username_id=username_id,
            rank_token=self.rank_token
        )
        tags = self.send_request(url)
        return tags

    def get_self_user_tags(self):
        return self.get_user_tags(self.user_id)

    def tag_feed(self, tag):
        userFeed = self.send_request(
            'feed/tag/' + str(tag) + '/?rank_token=' + str(self.rank_token) + '&ranked_content=true&')
        return userFeed

    def get_media_likers(self, media_id):
        likers = self.send_request('media/' + str(media_id) + '/likers/?')
        return likers

    def get_geo_media(self, username_id):
        locations = self.send_request('maps/user/' + str(username_id) + '/')
        return locations

    def get_self_geo_media(self):
        return self.get_geo_media(self.user_id)

    def fb_user_search(self, query):
        return fb_user_search(self, query)

    def search_users(self, query):
        return search_users(self, query)

    def search_username(self, username):
        return search_username(self, username)

    def search_tags(self, query):
        return search_tags(self, query)

    def search_location(self, query='', lat=None, lng=None):
        return search_location(self, query, lat, lng)

    def sync_from_adress_book(self, contacts):
        return self.send_request('address_book/link/?include=extra_display_name,thumbnails',
                                "contacts=" + json.dumps(contacts))

    def get_timeline(self):
        query = self.send_request(
            'feed/timeline/?rank_token=' + str(self.rank_token) + '&ranked_content=true&')
        return query

    def get_archive_feed(self):
        query = self.send_request(
            'feed/only_me_feed/?rank_token=' + str(self.rank_token) + '&ranked_content=true&')
        return query

    def get_user_feed(self, username_id, maxid='', minTimestamp=None):
        url = 'feed/user/{username_id}/?max_id={max_id}&min_timestamp={min_timestamp}&rank_token={rank_token}&ranked_content=true'.format(
            username_id=username_id,
            max_id=maxid,
            min_timestamp=minTimestamp,
            rank_token=self.rank_token
        )
        return self.send_request(url)

    def get_self_user_feed(self, maxid='', minTimestamp=None):
        return self.get_user_feed(self.user_id, maxid, minTimestamp)

    def get_hashtag_feed(self, hashtag_str, maxid=''):
        return self.send_request('feed/tag/' + hashtag_str + '/?max_id=' + str(
            maxid) + '&rank_token=' + self.rank_token + '&ranked_content=true&')

    def get_location_feed(self, location_id, maxid=''):
        return self.send_request('feed/location/' + str(location_id) + '/?max_id=' + str(
            maxid) + '&rank_token=' + self.rank_token + '&ranked_content=true&')

    def get_popular_feed(self):
        popularFeed = self.send_request(
            'feed/popular/?people_teaser_supported=1&rank_token={rank_token}&ranked_content=true&'.format(
                rank_token=self.rank_token
            ))
        return popularFeed

    def get_user_followings(self, username_id, maxid=''):
        url = 'friendships/{username_id}/following/?max_id={max_id}&ig_sig_key_version={sig_key}&rank_token={rank_token}'.format(
            username_id=username_id,
            max_id=maxid,
            sig_key=config.SIG_KEY_VERSION,
            rank_token=self.rank_token
        )
        return self.send_request(url)

    def get_self_users_following(self):
        return self.get_user_followings(self.user_id)

    def get_user_followers(self, username_id, maxid=''):
        if maxid == '':
            return self.send_request('friendships/' + str(username_id) + '/followers/?rank_token=' + self.rank_token)
        else:
            return self.send_request(
                'friendships/' + str(username_id) + '/followers/?rank_token=' + self.rank_token + '&max_id=' + str(
                    maxid))

    def get_self_user_followers(self):
        return self.get_user_followers(self.user_id)

    def like(self, media_id):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            '_csrftoken': self.token,
            'media_id': media_id
        })
        return self.send_request('media/' + str(media_id) + '/like/', self.generate_signature(data))

    def unlike(self, media_id):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            '_csrftoken': self.token,
            'media_id': media_id
        })
        return self.send_request('media/' + str(media_id) + '/unlike/', self.generate_signature(data))

    def get_media_comements(self, media_id):
        return self.send_request('media/' + str(media_id) + '/comments/?')

    def set_name_and_phone(self, name='', phone=''):
        return set_name_and_phone(self, name, phone)

    def get_direct_share(self):
        return self.send_request('direct_share/inbox/?')

    def follow(self, user_id):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            'user_id': user_id,
            '_csrftoken': self.token
        })
        return self.send_request('friendships/create/' + str(user_id) + '/', self.generate_signature(data))

    def unfollow(self, user_id):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            'user_id': user_id,
            '_csrftoken': self.token
        })
        return self.send_request('friendships/destroy/' + str(user_id) + '/', self.generate_signature(data))

    def block(self, user_id):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            'user_id': user_id,
            '_csrftoken': self.token
        })
        return self.send_request('friendships/block/' + str(user_id) + '/', self.generate_signature(data))

    def unblock(self, user_id):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            'user_id': user_id,
            '_csrftoken': self.token
        })
        return self.send_request('friendships/unblock/' + str(user_id) + '/', self.generate_signature(data))

    def user_friendship(self, user_id):
        data = json.dumps({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            'user_id': user_id,
            '_csrftoken': self.token
        })
        return self.send_request('friendships/show/' + str(user_id) + '/', self.generate_signature(data))

    def _prepare_recipients(self, users, thread_id=None, use_quotes=False):
        if not isinstance(users, list):
            print('Users must be an list')
            return False
        result = {'users': '[[{}]]'.format(','.join(users))}
        if thread_id:
            result['thread'] = '["{}"]'.format(thread_id) if use_quotes else '[{}]'.format(thread_id)
        return result

    def send_direct_item(self, item_type, users, **options):
        data = {
            '_uuid': self.uuid,
            '_uid': self.user_id,
            '_csrftoken': self.token,
            'client_context': self.generate_UUID(True),
            'action': 'send_item'
        }
        url = ''
        if item_type == 'links':
            data['link_text'] = options.get('text')
            data['link_urls'] = json.dumps(options.get('urls'))
            url = 'direct_v2/threads/broadcast/link/'
        elif item_type == 'message':
            data['text'] = options.get('text', '')
            url = 'direct_v2/threads/broadcast/text/'
        elif item_type == 'media_share':
            data['media_type'] = options.get('media_type', 'photo')
            data['text'] = options.get('text', '')
            data['media_id'] = options.get('media_id', '')
            url = 'direct_v2/threads/broadcast/media_share/'
        elif item_type == 'like':
            url = 'direct_v2/threads/broadcast/like/'
        elif item_type == 'hashtag':
            url = 'direct_v2/threads/broadcast/hashtag/'
            data['text'] = options.get('text', '')
            data['hashtag'] = options.get('hashtag', '')
        elif item_type == 'profile':
            url = 'direct_v2/threads/broadcast/profile/'
            data['profile_user_id'] = options.get('profile_user_id')
            data['text'] = options.get('text', '')
        recipients = self._prepare_recipients(users, thread_id=options.get('thread'), use_quotes=False)
        if not recipients:
            return False
        data['recipient_users'] = recipients.get('users')
        if recipients.get('thread'):
            data['thread_ids'] = recipients.get('thread')
        return self.send_request(url, data)

    def generate_signature(self, data):
        try:
            parsedData = urllib.parse.quote(data)
        except AttributeError:
            parsedData = urllib.quote(data)

        return 'ig_sig_key_version=' + config.SIG_KEY_VERSION + '&signed_body=' + hmac.new(
            config.IG_SIG_KEY.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest() + '.' + parsedData

    def generate_device_id(self, seed):
        volatile_seed = "12345"
        m = hashlib.md5()
        m.update(seed.encode('utf-8') + volatile_seed.encode('utf-8'))
        return 'android-' + m.hexdigest()[:16]

    def generate_UUID(self, uuid_type):
        generated_uuid = str(uuid.uuid4())
        if uuid_type:
            return generated_uuid
        else:
            return generated_uuid.replace('-', '')

    def get_liked_media(self, maxid=''):
        return self.send_request('feed/liked/?max_id=' + str(maxid))

    def get_total_followers(self, username_id, amount=None):
        sleep_track = 0
        followers = []
        next_max_id = ''
        self.get_username_info(username_id)
        if "user" in self.last_json:
            if amount:
                total_followers = amount
            else:
                total_followers = self.last_json["user"]['follower_count']
            if total_followers > 200000:
                print("Consider temporarily saving the result of this big operation. This will take a while.\n")
        else:
            return False
        with tqdm(total=total_followers, desc="Getting followers", leave=False) as pbar:
            while True:
                self.get_user_followers(username_id, next_max_id)
                temp = self.last_json
                try:
                    pbar.update(len(temp["users"]))
                    for item in temp["users"]:
                        followers.append(item)
                        sleep_track += 1
                        if sleep_track >= 20000:
                            sleep_time = randint(120, 180)
                            print("\nWaiting %.2f min. due to too many requests." % float(sleep_time / 60))
                            time.sleep(sleep_time)
                            sleep_track = 0
                    if len(temp["users"]) == 0 or len(followers) >= total_followers:
                        return followers[:total_followers]
                except Exception:
                    return followers[:total_followers]
                if temp["big_list"] is False:
                    return followers[:total_followers]
                next_max_id = temp["next_max_id"]

    def get_total_followings(self, username_id, amount=None):
        sleep_track = 0
        following = []
        next_max_id = ''
        self.get_username_info(username_id)
        if "user" in self.last_json:
            if amount:
                total_following = amount
            else:
                total_following = self.last_json["user"]['following_count']
            if total_following > 200000:
                print("Consider temporarily saving the result of this big operation. This will take a while.\n")
        else:
            return False
        with tqdm(total=total_following, desc="Getting following", leave=False) as pbar:
            while True:
                self.get_user_followings(username_id, next_max_id)
                temp = self.last_json
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
                except Exception:
                    return following[:total_following]
                if temp["big_list"] is False:
                    return following[:total_following]
                next_max_id = temp["next_max_id"]

    def get_total_user_feed(self, username_id, minTimestamp=None):
        user_feed = []
        next_max_id = ''
        while 1:
            self.get_user_feed(username_id, next_max_id, minTimestamp)
            temp = self.last_json
            if "items" not in temp:  # maybe user is private, (we have not access to posts)
                return []
            for item in temp["items"]:
                user_feed.append(item)
            if "more_available" not in temp or temp["more_available"] is False:
                return user_feed
            next_max_id = temp["next_max_id"]

    def get_total_hashtag_feed(self, hashtag_str, amount=100):
        hashtag_feed = []
        next_max_id = ''

        with tqdm(total=amount, desc="Getting hashtag medias", leave=False) as pbar:
            while True:
                self.get_hashtag_feed(hashtag_str, next_max_id)
                temp = self.last_json
                try:
                    pbar.update(len(temp["items"]))
                    for item in temp["items"]:
                        hashtag_feed.append(item)
                    if len(temp["items"]) == 0 or len(hashtag_feed) >= amount:
                        return hashtag_feed[:amount]
                except Exception:
                    return hashtag_feed[:amount]
                next_max_id = temp["next_max_id"]

    def get_total_self_user_feed(self, min_timestamp=None):
        return self.get_total_user_feed(self.user_id, min_timestamp)

    def get_total_self_followers(self):
        return self.get_total_followers(self.user_id)

    def get_total_self_followings(self):
        return self.get_total_followings(self.user_id)

    def get_total_liked_media(self, scan_rate=1):
        next_id = ''
        liked_items = []
        for _ in range(0, scan_rate):
            temp = self.get_liked_media(next_id)
            temp = self.last_json
            next_id = temp["next_max_id"]
            for item in temp["items"]:
                liked_items.append(item)
        return liked_items
