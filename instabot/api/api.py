import hashlib
import hmac
import json
import logging
import os
import sys
import time
import uuid
import random

try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

import requests
import requests.utils
import six.moves.urllib as urllib
from tqdm import tqdm

from . import config, devices
from .api_photo import configure_photo, download_photo, upload_photo
from .api_video import configure_video, download_video, upload_video
from .api_story import download_story, upload_story_photo, configure_story
from .prepare import delete_credentials, get_credentials

PY2 = sys.version_info[0] == 2


class API(object):
    def __init__(self, device=None, base_path=''):
        # Setup device and user_agent
        device = device or devices.DEFAULT_DEVICE
        self.device_settings = devices.DEVICES[device]
        self.user_agent = config.USER_AGENT_BASE.format(**self.device_settings)
        self.base_path = base_path

        self.is_logged_in = False
        self.last_response = None
        self.total_requests = 0

        # Setup logging
        self.logger = logging.getLogger('[instabot_{}]'.format(id(self)))

        if not os.path.exists("./config/"):
            os.makedirs("./config/")  # create base_path if not exists

        log_filename = os.path.join(base_path, 'instabot.log')
        fh = logging.FileHandler(filename=log_filename)
        fh.setLevel(logging.INFO)
        fh.setFormatter(logging.Formatter('%(asctime)s %(message)s'))

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'))

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        self.logger.setLevel(logging.DEBUG)

        self.last_json = None

    def set_user(self, username, password):
        self.username = username
        self.password = password
        self.uuid = self.generate_UUID(uuid_type=True)

    def login(self, username=None, password=None, force=False, proxy=None,
              use_cookie=False, cookie_fname=None):
        if password is None:
            username, password = get_credentials(username=username)

        self.device_id = self.generate_device_id(self.get_seed(username, password))
        self.proxy = proxy
        self.set_user(username, password)

        if not cookie_fname:
            cookie_fname = "{username}_cookie.txt".format(username=username)
            cookie_fname = os.path.join(self.base_path, cookie_fname)

        cookie_is_loaded = False
        if use_cookie:
            try:
                self.load_cookie(cookie_fname)
                cookie_is_loaded = True
                self.is_logged_in = True
                self.set_proxy()  # Only happens if `self.proxy`
                self.logger.info("Logged-in successfully as '{}' using the cookie!".format(self.username))
                return True
            except Exception:
                print("The cookie is not found, but don't worry `instabot`"
                      " will create it for you using your login details.")

        if not cookie_is_loaded and (not self.is_logged_in or force):
            self.session = requests.Session()
            self.set_proxy()  # Only happens if `self.proxy`
            url = 'si/fetch_headers/?challenge_type=signup&guid={uuid}'
            url = url.format(uuid=self.generate_UUID(False))
            if self.send_request(url, login=True):
                data = json.dumps({
                    'phone_id': self.generate_UUID(True),
                    '_csrftoken': self.token,
                    'username': self.username,
                    'guid': self.uuid,
                    'device_id': self.device_id,
                    'password': self.password,
                    'login_attempt_count': '0',
                })

                if self.send_request('accounts/login/', data, True):
                    self.is_logged_in = True
                    self.logger.info("Logged-in successfully as '{}'!".format(self.username))
                    if use_cookie:
                        self.save_cookie(cookie_fname)
                        self.logger.info("Saved cookie!")
                    return True
                else:
                    self.logger.info("Username or password is incorrect.")
                    delete_credentials()
                    return False

    def load_cookie(self, fname):
        # Python2 compatibility
        if PY2:
            FileNotFoundError = IOError

        try:
            with open(fname, 'r') as f:
                self.session = requests.Session()
                self.session.cookies = requests.utils.cookiejar_from_dict(json.load(f))
            cookie_username = self.cookie_dict['ds_user']
            assert cookie_username == self.username
        except FileNotFoundError:
            raise Exception('Cookie file `{}` not found'.format(fname))
        except (TypeError, EOFError):
            os.remove(fname)
            msg = ('An error occured opening the cookie `{}`, '
                   'it will be removed an recreated.')
            raise Exception(msg.format(fname))
        except AssertionError:
            msg = 'The loaded cookie was for {} instead of {}.'
            raise Exception(msg.format(cookie_username, self.username))

    def save_cookie(self, fname):
        with open(fname, 'w') as f:
            json.dump(requests.utils.dict_from_cookiejar(self.session.cookies), f)

    def logout(self, *args, **kwargs):
        if not self.is_logged_in:
            return True
        self.is_logged_in = not self.send_request('accounts/logout/')
        return not self.is_logged_in

    def set_proxy(self):
        if self.proxy:
            parsed = urllib.parse.urlparse(self.proxy)
            scheme = 'http://' if not parsed.scheme else ''
            self.session.proxies['http'] = scheme + self.proxy
            self.session.proxies['https'] = scheme + self.proxy

    def send_request(self, endpoint, post=None, login=False, with_signature=True):
        if (not self.is_logged_in and not login):
            msg = "Not logged in!"
            self.logger.critical(msg)
            raise Exception(msg)

        self.session.headers.update(config.REQUEST_HEADERS)
        self.session.headers.update({'User-Agent': self.user_agent})
        try:
            self.total_requests += 1
            if post is not None:  # POST
                if with_signature:
                    # Only `send_direct_item` doesn't need a signature
                    post = self.generate_signature(post)
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
            try:
                self.last_json = json.loads(response.text)
                return True
            except JSONDecodeError:
                return False
        else:
            if response.status_code != 404 and response.status_code != "404":
                self.logger.error("Request returns {} error!".format(response.status_code))
            try:
                response_data = json.loads(response.text)
                if "feedback_required" in str(response_data.get('message')):
                    self.logger.error("ATTENTION!: `feedback_required`, your action could have been blocked")
                    return "feedback_required"
            except ValueError:
                self.logger.error("Error checking for `feedback_required`, response text is not JSON")

            if response.status_code == 429:
                sleep_minutes = 5
                self.logger.warning(
                    "That means 'too many requests'. I'll go to sleep "
                    "for {} minutes.".format(sleep_minutes))
                time.sleep(sleep_minutes * 60)
            elif response.status_code == 400:
                response_data = json.loads(response.text)

                # PERFORM Interactive Two-Factor Authentication
                if response_data.get('two_factor_required'):
                    self.logger.info("Two-factor authentication required")
                    two_factor_code = input("Enter 2FA verification code: ")
                    two_factor_id = response_data['two_factor_info']['two_factor_identifier']

                    login = self.session.post(config.API_URL + 'accounts/two_factor_login/',
                                              data={'username': self.username,
                                                    'verification_code': two_factor_code,
                                                    'two_factor_identifier': two_factor_id,
                                                    'password': self.password,
                                                    'device_id': self.device_id,
                                                    'ig_sig_key_version': 4
                                                    },
                                              allow_redirects=True)

                    if login.status_code == 200:
                        resp_json = json.loads(login.text)
                        if resp_json['status'] != 'ok':
                            if 'message' in resp_json:
                                self.logger.error("Login error: {}".format(resp_json['message']))
                            else:
                                self.logger.error(
                                    "Login error: \"{}\" status and message {}.".format(resp_json['status'],
                                                                                        login.text))
                            return False
                        return True
                    else:
                        self.logger.error("Two-factor authentication request returns {} error with message {} !".format(
                            login.status_code, login.text))
                        return False
                # End of Interactive Two-Factor Authentication
                else:
                    msg = "Instagram's error message: {}"
                    self.logger.info(msg.format(response_data.get('message')))
                    if 'error_type' in response_data:
                        msg = 'Error type: {}'.format(response_data['error_type'])
                    self.logger.info(msg)

            # For debugging
            try:
                self.last_response = response
                self.last_json = json.loads(response.text)
            except Exception:
                pass
            return False

    @property
    def cookie_dict(self):
        return self.session.cookies.get_dict()

    @property
    def token(self):
        return self.cookie_dict['csrftoken']

    @property
    def user_id(self):
        return self.cookie_dict['ds_user_id']

    @property
    def rank_token(self):
        return "{}_{}".format(self.user_id, self.uuid)

    @property
    def default_data(self):
        return {
            '_uuid': self.uuid,
            '_uid': self.user_id,
            '_csrftoken': self.token,
        }

    def json_data(self, data=None):
        """Adds the default_data to data and dumps it to a json."""
        if data is None:
            data = {}
        data.update(self.default_data)
        return json.dumps(data)

    def sync_features(self):
        data = self.json_data({'id': self.user_id, 'experiments': config.EXPERIMENTS})
        return self.send_request('qe/sync/', data)

    def auto_complete_user_list(self):
        return self.send_request('friendships/autocomplete_user_list/')

    def get_timeline_feed(self):
        """ Returns 8 medias from timeline feed of logged user."""
        return self.send_request('feed/timeline/')

    def get_megaphone_log(self):
        return self.send_request('megaphone/log/')

    def expose(self):
        data = self.json_data({
            'id': self.user_id,
            'experiment': 'ig_android_profile_contextual_feed'
        })
        return self.send_request('qe/expose/', data)

    def upload_photo(self, photo, caption=None, upload_id=None, from_video=False):
        return upload_photo(self, photo, caption, upload_id, from_video)

    def download_photo(self, media_id, filename, media=False, folder='photos'):
        return download_photo(self, media_id, filename, media, folder)

    def configure_photo(self, upload_id, photo, caption=''):
        return configure_photo(self, upload_id, photo, caption)

    def download_story(self, filename, story_url, username):
        return download_story(self, filename, story_url, username)

    def upload_story_photo(self, photo, upload_id=None):
        return upload_story_photo(self, photo, upload_id)

    def configure_story(self, upload_id, photo):
        return configure_story(self, upload_id, photo)

    def upload_video(self, photo, caption=None, upload_id=None):
        return upload_video(self, photo, caption, upload_id)

    def download_video(self, media_id, filename, media=False, folder='video'):
        return download_video(self, media_id, filename, media, folder)

    def configure_video(self, upload_id, video, thumbnail, width, height, duration, caption=''):
        return configure_video(self, upload_id, video, thumbnail, width, height, duration, caption)

    def edit_media(self, media_id, captionText=''):
        data = self.json_data({'caption_text': captionText})
        url = 'media/{media_id}/edit_media/'.format(media_id=media_id)
        return self.send_request(url, data)

    def remove_self_tag(self, media_id):
        data = self.json_data()
        url = 'media/{media_id}/remove/'.format(media_id=media_id)
        return self.send_request(url, data)

    def media_info(self, media_id):
        # data = self.json_data({'media_id': media_id})
        url = 'media/{media_id}/info/'.format(media_id=media_id)
        return self.send_request(url)

    def archive_media(self, media, undo=False):
        action = 'only_me' if not undo else 'undo_only_me'
        data = self.json_data({'media_id': media['id']})
        url = 'media/{media_id}/{action}/?media_type={media_type}'.format(
            media_id=media['id'],
            action=action,
            media_type=media['media_type']
        )
        return self.send_request(url, data)

    def delete_media(self, media):
        data = self.json_data({'media_id': media.get('id')})
        url = 'media/{media_id}/delete/'.format(media_id=media.get('id'))
        return self.send_request(url, data)

    def change_password(self, new_password):
        data = self.json_data({
            'old_password': self.password,
            'new_password1': new_password,
            'new_password2': new_password
        })
        return self.send_request('accounts/change_password/', data)

    def explore(self):
        return self.send_request('discover/explore/')

    def comment(self, media_id, comment_text):
        data = self.json_data({'comment_text': comment_text})
        url = 'media/{media_id}/comment/'.format(media_id=media_id)
        return self.send_request(url, data)

    def reply_to_comment(self, media_id, comment_text, parent_comment_id):
        data = self.json_data({'comment_text': comment_text, 'replied_to_comment_id': parent_comment_id})
        url = 'media/{media_id}/comment/'.format(media_id=media_id)
        return self.send_request(url, data)

    def delete_comment(self, media_id, comment_id):
        data = self.json_data()
        url = 'media/{media_id}/comment/{comment_id}/delete/'
        url = url.format(media_id=media_id, comment_id=comment_id)
        return self.send_request(url, data)

    def get_username_info(self, user_id):
        url = 'users/{user_id}/info/'.format(user_id=user_id)
        return self.send_request(url)

    def get_self_username_info(self):
        return self.get_username_info(self.user_id)

    def get_recent_activity(self):
        return self.send_request('news/inbox/?')

    def get_following_recent_activity(self):
        return self.send_request('news/?')

    def getv2Inbox(self):
        return self.send_request('direct_v2/inbox/?')

    def get_user_tags(self, user_id):
        url = 'usertags/{user_id}/feed/?rank_token={rank_token}&ranked_content=true&'
        url = url.format(user_id=user_id, rank_token=self.rank_token)
        return self.send_request(url)

    def get_self_user_tags(self):
        return self.get_user_tags(self.user_id)

    def tag_feed(self, tag):
        url = 'feed/tag/{tag}/?rank_token={rank_token}&ranked_content=true&'
        return self.send_request(url.format(tag=tag, rank_token=self.rank_token))

    def get_comment_likers(self, comment_id):
        url = 'media/{comment_id}/comment_likers/?'.format(comment_id=comment_id)
        return self.send_request(url)

    def get_media_likers(self, media_id):
        url = 'media/{media_id}/likers/?'.format(media_id=media_id)
        return self.send_request(url)

    def get_geo_media(self, user_id):
        url = 'maps/user/{user_id}/'.format(user_id=user_id)
        return self.send_request(url)

    def get_self_geo_media(self):
        return self.get_geo_media(self.user_id)

    def sync_from_adress_book(self, contacts):
        url = 'address_book/link/?include=extra_display_name,thumbnails'
        return self.send_request(url, 'contacts=' + json.dumps(contacts))

    def get_timeline(self):
        url = 'feed/timeline/?rank_token={rank_token}&ranked_content=true&'
        return self.send_request(url.format(rank_token=self.rank_token))

    def get_archive_feed(self):
        url = 'feed/only_me_feed/?rank_token={rank_token}&ranked_content=true&'
        return self.send_request(url.format(rank_token=self.rank_token))

    def get_user_feed(self, user_id, max_id='', min_timestamp=None):
        url = 'feed/user/{user_id}/?max_id={max_id}&min_timestamp={min_timestamp}&rank_token={rank_token}&ranked_content=true'
        url = url.format(
            user_id=user_id,
            max_id=max_id,
            min_timestamp=min_timestamp,
            rank_token=self.rank_token
        )
        return self.send_request(url)

    def get_self_user_feed(self, max_id='', min_timestamp=None):
        return self.get_user_feed(self.user_id, max_id, min_timestamp)

    def get_hashtag_feed(self, hashtag, max_id=''):
        url = 'feed/tag/{hashtag}/?max_id={max_id}&rank_token={rank_token}&ranked_content=true&'
        url = url.format(
            hashtag=hashtag,
            max_id=max_id,
            rank_token=self.rank_token
        )
        return self.send_request(url)

    def get_location_feed(self, location_id, max_id=''):
        url = 'feed/location/{location_id}/?max_id={max_id}&rank_token={rank_token}&ranked_content=true&'
        url = url.format(
            location_id=location_id,
            max_id=max_id,
            rank_token=self.rank_token
        )
        return self.send_request(url)

    def get_popular_feed(self):
        url = 'feed/popular/?people_teaser_supported=1&rank_token={rank_token}&ranked_content=true&'
        return self.send_request(url.format(rank_token=self.rank_token))

    def get_user_followings(self, user_id, max_id=''):
        url = 'friendships/{user_id}/following/?max_id={max_id}&ig_sig_key_version={sig_key}&rank_token={rank_token}'
        url = url.format(
            user_id=user_id,
            max_id=max_id,
            sig_key=config.SIG_KEY_VERSION,
            rank_token=self.rank_token
        )
        return self.send_request(url)

    def get_self_users_following(self):
        return self.get_user_followings(self.user_id)

    def get_user_followers(self, user_id, max_id=''):
        url = 'friendships/{user_id}/followers/?rank_token={rank_token}'
        url = url.format(user_id=user_id, rank_token=self.rank_token)
        if max_id:
            url += '&max_id={max_id}'.format(max_id=max_id)
        return self.send_request(url)

    def get_self_user_followers(self):
        return self.followers

    def like_comment(self, comment_id):
        data = self.json_data()
        url = 'media/{comment_id}/comment_like/'.format(comment_id=comment_id)
        return self.send_request(url, data)

    def unlike_comment(self, comment_id):
        data = self.json_data()
        url = 'media/{comment_id}/comment_unlike/'.format(comment_id=comment_id)
        return self.send_request(url, data)

    def like(self, media_id):
        data = self.json_data({'media_id': media_id})
        url = 'media/{media_id}/like/'.format(media_id=media_id)
        return self.send_request(url, data)

    def unlike(self, media_id):
        data = self.json_data({'media_id': media_id})
        url = 'media/{media_id}/unlike/'.format(media_id=media_id)
        return self.send_request(url, data)

    def get_media_comments(self, media_id, max_id=''):
        url = 'media/{media_id}/comments/'.format(media_id=media_id)
        if max_id:
            url += '?max_id={max_id}'.format(max_id=max_id)
        return self.send_request(url)

    def get_direct_share(self):
        return self.send_request('direct_share/inbox/?')

    def follow(self, user_id):
        data = self.json_data({'user_id': user_id})
        url = 'friendships/create/{user_id}/'.format(user_id=user_id)
        return self.send_request(url, data)

    def unfollow(self, user_id):
        data = self.json_data({'user_id': user_id})
        url = 'friendships/destroy/{user_id}/'.format(user_id=user_id)
        return self.send_request(url, data)

    def block(self, user_id):
        data = self.json_data({'user_id': user_id})
        url = 'friendships/block/{user_id}/'.format(user_id=user_id)
        return self.send_request(url, data)

    def unblock(self, user_id):
        data = self.json_data({'user_id': user_id})
        url = 'friendships/unblock/{user_id}/'.format(user_id=user_id)
        return self.send_request(url, data)

    def user_friendship(self, user_id):
        data = self.json_data({'user_id': user_id})
        url = 'friendships/show/{user_id}/'.format(user_id=user_id)
        return self.send_request(url, data)

    @staticmethod
    def _prepare_recipients(users, thread_id=None, use_quotes=False):
        if not isinstance(users, list):
            print('Users must be an list')
            return False
        result = {'users': '[[{}]]'.format(','.join(users))}
        if thread_id:
            template = '["{}"]' if use_quotes else '[{}]'
            result['thread'] = template.format(thread_id)
        return result

    def send_direct_item(self, item_type, users, **options):
        data = {
            'client_context': self.generate_UUID(True),
            'action': 'send_item'
        }

        url = 'direct_v2/threads/broadcast/{}/'.format(item_type)
        text = options.get('text', '')
        if item_type == 'link':
            data['link_text'] = text
            data['link_urls'] = json.dumps(options.get('urls'))
        elif item_type == 'text':
            data['text'] = text
        elif item_type == 'media_share':
            data['text'] = text
            data['media_type'] = options.get('media_type', 'photo')
            data['media_id'] = options.get('media_id', '')
        elif item_type == 'hashtag':
            data['text'] = text
            data['hashtag'] = options.get('hashtag', '')
        elif item_type == 'profile':
            data['text'] = text
            data['profile_user_id'] = options.get('profile_user_id')

        recipients = self._prepare_recipients(users, options.get('thread'), use_quotes=False)
        if not recipients:
            return False
        data['recipient_users'] = recipients.get('users')
        if recipients.get('thread'):
            data['thread_ids'] = recipients.get('thread')
        data.update(self.default_data)
        return self.send_request(url, data, with_signature=False)

    @staticmethod
    def generate_signature(data):
        body = hmac.new(config.IG_SIG_KEY.encode('utf-8'), data.encode('utf-8'),
                        hashlib.sha256).hexdigest() + '.' + urllib.parse.quote(data)
        signature = 'ig_sig_key_version={sig_key}&signed_body={body}'
        return signature.format(sig_key=config.SIG_KEY_VERSION, body=body)

    @staticmethod
    def generate_device_id(seed):
        volatile_seed = "12345"
        m = hashlib.md5()
        m.update(seed.encode('utf-8') + volatile_seed.encode('utf-8'))
        return 'android-' + m.hexdigest()[:16]

    @staticmethod
    def get_seed(*args):
        m = hashlib.md5()
        m.update(b''.join([arg.encode('utf-8') for arg in args]))
        return m.hexdigest()

    @staticmethod
    def generate_UUID(uuid_type):
        generated_uuid = str(uuid.uuid4())
        if uuid_type:
            return generated_uuid
        else:
            return generated_uuid.replace('-', '')

    def get_liked_media(self, max_id=''):
        url = 'feed/liked/?max_id={max_id}'.format(max_id=max_id)
        return self.send_request(url)

    def get_total_followers_or_followings(self,
                                          user_id,
                                          amount=None,
                                          which='followers',
                                          filter_private=False,
                                          filter_business=False,
                                          filter_verified=False,
                                          usernames=False,
                                          to_file=None,
                                          overwrite=False):
        from io import StringIO

        if which == 'followers':
            key = 'follower_count'
            get = self.get_user_followers
        elif which == 'followings':
            key = 'following_count'
            get = self.get_user_followings

        sleep_track = 0
        result = []
        next_max_id = ''
        self.get_username_info(user_id)
        username_info = self.last_json
        if "user" in username_info:
            total = amount or username_info["user"][key]

            if total > 200000:
                print("Consider temporarily saving the result of this big "
                      "operation. This will take a while.\n")
        else:
            return False
        if filter_business:
            print("--> You are going to filter business accounts. This will take time! <--")
            from random import random
        if to_file is not None:
            if os.path.isfile(to_file):
                if not overwrite:
                    print("File `{}` already exists. Not overwriting.".format(to_file))
                    return False
                else:
                    print("Overwriting file `{}`".format(to_file))
            with open(to_file, 'w'):
                pass
        desc = "Getting {} of {}".format(which, user_id)
        with tqdm(total=total, desc=desc, leave=True) as pbar:
            while True:
                get(user_id, next_max_id)
                last_json = self.last_json
                try:
                    with open(to_file, 'a') if to_file is not None else StringIO() as f:
                        for item in last_json["users"]:
                            if filter_private and item['is_private']:
                                continue
                            if filter_business:
                                time.sleep(2 * random())
                                self.get_username_info(item['pk'])
                                item_info = self.last_json
                                if item_info['user']['is_business']:
                                    continue
                            if filter_verified and item['is_verified']:
                                continue
                            if to_file is not None:
                                if usernames:
                                    f.write("{}\n".format(item['username']))
                                else:
                                    f.write("{}\n".format(item['pk']))
                            result.append(item)
                            pbar.update(1)
                            sleep_track += 1
                            if sleep_track >= 20000:
                                sleep_time = random.uniform(120, 180)
                                msg = "\nWaiting {:.2f} min. due to too many requests."
                                print(msg.format(sleep_time / 60))
                                time.sleep(sleep_time)
                                sleep_track = 0
                    if not last_json["users"] or len(result) >= total:
                        return result[:total]
                except Exception as e:
                    print("ERROR: {}".format(e))
                    return result[:total]

                if last_json["big_list"] is False:
                    return result[:total]

                next_max_id = last_json.get("next_max_id", "")

    def get_total_followers(self, user_id, amount=None):
        return self.get_total_followers_or_followings(
            user_id, amount, 'followers')

    def get_total_followings(self, user_id, amount=None):
        return self.get_total_followers_or_followings(
            user_id, amount, 'followings')

    def get_total_user_feed(self, user_id, min_timestamp=None):
        return self.get_last_user_feed(user_id, amount=float('inf'), min_timestamp=min_timestamp)

    def get_last_user_feed(self, user_id, amount, min_timestamp=None):
        user_feed = []
        next_max_id = ''
        while True:
            if len(user_feed) >= float(amount):
                # one request returns max 13 items
                return user_feed[:amount]
            self.get_user_feed(user_id, next_max_id, min_timestamp)
            last_json = self.last_json
            if 'items' not in last_json:
                return user_feed
            user_feed += last_json["items"]
            if not last_json.get("more_available"):
                return user_feed
            next_max_id = last_json.get("next_max_id", "")

    def get_total_hashtag_feed(self, hashtag_str, amount=100):
        hashtag_feed = []
        next_max_id = ''

        with tqdm(total=amount, desc="Getting hashtag media.", leave=False) as pbar:
            while True:
                self.get_hashtag_feed(hashtag_str, next_max_id)
                last_json = self.last_json
                if 'items' not in last_json:
                    return hashtag_feed[:amount]
                items = last_json['items']
                try:
                    pbar.update(len(items))
                    hashtag_feed += items
                    if not items or len(hashtag_feed) >= amount:
                        return hashtag_feed[:amount]
                except Exception:
                    return hashtag_feed[:amount]
                next_max_id = last_json.get("next_max_id", "")

    def get_total_self_user_feed(self, min_timestamp=None):
        return self.get_total_user_feed(self.user_id, min_timestamp)

    def get_total_self_followers(self):
        return self.get_total_followers(self.user_id)

    def get_total_self_followings(self):
        return self.get_total_followings(self.user_id)

    def get_total_liked_media(self, scan_rate=1):
        next_id = ''
        liked_items = []
        for _ in range(scan_rate):
            self.get_liked_media(next_id)
            last_json = self.last_json
            next_id = last_json.get("next_max_id", "")
            liked_items += last_json["items"]
        return liked_items

    def remove_profile_picture(self):
        data = self.json_data()
        return self.send_request('accounts/remove_profile_picture/', data)

    def set_private_account(self):
        data = self.json_data()
        return self.send_request('accounts/set_private/', data)

    def set_public_account(self):
        data = self.json_data()
        return self.send_request('accounts/set_public/', data)

    def set_name_and_phone(self, name='', phone=''):
        data = self.json_data({'first_name': name, 'phone_number': phone})
        return self.send_request('accounts/set_phone_and_name/', data)

    def get_profile_data(self):
        data = self.json_data()
        return self.send_request('accounts/current_user/?edit=true', data)

    def edit_profile(self, url, phone, first_name, biography, email, gender):
        data = self.json_data({
            'external_url': url,
            'phone_number': phone,
            'username': self.username,
            'full_name': first_name,
            'biography': biography,
            'email': email,
            'gender': gender,
        })
        return self.send_request('accounts/edit_profile/', data)

    def fb_user_search(self, query):
        url = 'fbsearch/topsearch/?context=blended&query={query}&rank_token={rank_token}'
        url = url.format(query=query, rank_token=self.rank_token)
        return self.send_request(url)

    def search_users(self, query):
        url = 'users/search/?ig_sig_key_version={sig_key}&is_typeahead=true&query={query}&rank_token={rank_token}'
        url = url.format(
            sig_key=config.SIG_KEY_VERSION,
            query=query,
            rank_token=self.rank_token
        )
        return self.send_request(url)

    def search_username(self, username):
        url = 'users/{username}/usernameinfo/'.format(username=username)
        return self.send_request(url)

    def search_tags(self, query):
        url = 'tags/search/?is_typeahead=true&q={query}&rank_token={rank_token}'
        url = url.format(query=query, rank_token=self.rank_token)
        return self.send_request(url)

    def search_location(self, query='', lat=None, lng=None):
        url = 'fbsearch/places/?rank_token={rank_token}&query={query}&lat={lat}&lng={lng}'
        url = url.format(rank_token=self.rank_token, query=query, lat=lat, lng=lng)
        return self.send_request(url)

    def get_user_reel(self, user_id):
        url = 'feed/user/{}/reel_media/'.format(user_id)
        return self.send_request(url)

    def get_users_reel(self, user_ids):
        """
        Input: user_ids - a list of user_id
        Output: dictionary: user_id - stories data.
        Basically, for each user output the same as after self.get_user_reel
        """
        url = 'feed/reels_media/'
        res = self.send_request(
            url,
            post=self.json_data({
                'user_ids': [str(x) for x in user_ids]
            })
        )
        if res:
            if "reels" in self.last_json:
                return self.last_json["reels"]
            return []
        return []

    def see_reels(self, reels):
        """
            Input - the list of reels jsons
            They can be aquired by using get_users_reel() or get_user_reel() methods
        """
        if not isinstance(reels, list):
            reels = [reels]

        story_seen = {}
        now = int(time.time())
        for i, story in enumerate(sorted(reels, key=lambda m: m['taken_at'], reverse=True)):
            story_seen_at = now - min(i + 1 + random.randint(0, 2), max(0, now - story['taken_at']))
            story_seen[
                '{0!s}_{1!s}'.format(story['id'], story['user']['pk'])
            ] = [
                '{0!s}_{1!s}'.format(story['taken_at'], story_seen_at)
            ]

        data = self.json_data({
            'reels': story_seen,
            '_csrftoken': self.token,
            '_uuid': self.uuid,
            '_uid': self.user_id
        })
        data = self.generate_signature(data)
        return self.session.post('https://i.instagram.com/api/v2/' + 'media/seen/', data=data).ok

    def get_user_stories(self, user_id):
        url = 'feed/user/{}/story/'.format(user_id)
        return self.send_request(url)

    def get_self_story_viewers(self, story_id):

        url = 'media/{}/list_reel_media_viewer/?supported_capabilities_new={}'.format(story_id,
                                                                                      config.SUPPORTED_CAPABILITIES)
        return self.send_request(url)

    def get_tv_suggestions(self):
        url = 'igtv/tv_guide/'
        return self.send_request(url)

    def get_hashtag_stories(self, hashtag):
        url = 'tags/{}/story/'.format(hashtag)
        return self.send_request(url)

    def follow_hashtag(self, hashtag):
        data = self.json_data({})
        url = 'tags/follow/{}/'.format(hashtag)
        return self.send_request(url, data)

    def unfollow_hashtag(self, hashtag):
        data = self.json_data({})
        url = 'tags/unfollow/{}/'.format(hashtag)
        return self.send_request(url, data)

    def get_tags_followed_by_user(self, user_id):
        url = 'users/{}/following_tags_info/'.format(user_id)
        return self.send_request(url)

    def get_hashtag_sections(self, hashtag):
        data = self.json_data({'supported_tabs': "['top','recent','places']", 'include_persistent': 'true'})
        url = 'tags/{}/sections/'.format(hashtag)
        return self.send_request(url, data)

    def get_media_insight(self, media_id):
        url = 'insights/media_organic_insights/{}/?ig_sig_key_version={}'.format(media_id, config.IG_SIG_KEY)
        return self.send_request(url)

    def get_self_insight(self):
        url = 'insights/account_organic_insights/?show_promotions_in_landing_page=true&first={}'.format()  # todo
        return self.send_request(url)

    def save_media(self, media_id):
        data = self.json_data()
        url = 'media/{}/save/'.format(media_id)
        return self.send_request(url, data)

    def unsave_media(self, media_id):
        data = self.json_data()
        url = 'media/{}/unsave/'.format(media_id)
        return self.send_request(url, data)

    def get_saved_medias(self):
        url = 'feed/saved/'
        return self.send_request(url)

    def mute_user(self, user, mute_story=False, mute_posts=False):
        data_dict = {}
        if mute_posts:
            data_dict['target_posts_author_id'] = user
        if mute_story:
            data_dict['target_reel_author_id'] = user
        data = self.json_data(data_dict)
        url = 'friendships/mute_posts_or_story_from_follow/'
        return self.send_request(url, data)

    def unmute_user(self, user, unmute_posts=False, unmute_stories=False):
        data_dict = {}
        if unmute_posts:
            data_dict['target_posts_author_id'] = user
        if unmute_stories:
            data_dict['target_reel_author_id'] = user
        data = self.json_data(data_dict)
        url = 'friendships/unmute_posts_or_story_from_follow/'
        return self.send_request(url, data)

    def get_pending_friendships(self):
        """Get pending follow requests"""
        url = 'friendships/pending/'
        return self.send_request(url)

    def approve_pending_friendship(self, user_id):
        data = self.json_data({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            'user_id': user_id,
            '_csrftoken': self.token
        })
        url = 'friendships/approve/{}/'.format(user_id)
        return self.send_request(url, post=data)

    def reject_pending_friendship(self, user_id):
        data = self.json_data({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            'user_id': user_id,
            '_csrftoken': self.token
        })
        url = 'friendships/ignore/{}/'.format(user_id)
        return self.send_request(url, post=data)

    def get_pending_inbox(self):
        url = 'direct_v2/pending_inbox/?persistentBadging=true&use_unified_inbox=true'
        return self.send_request(url)

    def approve_pending_thread(self, thread_id):
        data = self.json_data({
            '_uuid': self.uuid,
            '_uid': self.user_id,
            '_csrftoken': self.token
        })
        url = 'direct_v2/threads/{}/approve/'.format(thread_id)
        return self.send_request(url, post=data)
