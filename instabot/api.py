import requests
import time
import random
import config

from api_info import get_profile_info, get_following, get_user_id_by_username
from api_feed import get_feed
from prepare import get_credentials
from requests.exceptions import RequestException


class API:

    user_agent = config.USER_AGENT
    accept_language = config.ACCEPT_LANGUAGE
    url = 'https://www.instagram.com/'
    url_tag = 'https://www.instagram.com/explore/tags/'
    url_like = 'https://www.instagram.com/web/likes/%s/like/'
    url_unlike = 'https://www.instagram.com/web/likes/%s/unlike/'
    url_comment = 'https://www.instagram.com/web/comments/%s/add/'
    url_follow = 'https://www.instagram.com/web/friendships/%s/follow/'
    url_unfollow = 'https://www.instagram.com/web/friendships/%s/unfollow/'
    url_login = 'https://www.instagram.com/accounts/login/ajax/'
    url_logout = 'https://www.instagram.com/accounts/logout/'
    url_media_info = 'https://www.instagram.com/p/%s/?__a=1'
    url_user_info = 'https://www.instagram.com/%s/?__a=1'

    def __init__(self):
        self.session = requests.Session()
        self.user_login = None
        self.user_password = None
        self.login_post = None
        self.csrftoken = None
        self.login_status = None

    def login(self, login=None, password=None):
        '''
        If login or password is not passed function will take them
        from secret.txt
        '''
        if login is not None and password is not None:
            self.user_login = login
            self.user_password = password
        else:
            login, password = get_credentials()
            self.user_login = login.lower()
            self.user_password = password

        self.login_post = {'username': self.user_login,
                           'password': self.user_password}

        self.session.cookies.update(config.BASE_COOKIE)
        self.session.headers.update(config.BASE_HEADER)
        r = self.session.get(self.url)
        self.session.headers.update({'X-CSRFToken': r.cookies['csrftoken']})
        time.sleep(2 * random.random())
        login = self.session.post(self.url_login, data=self.login_post,
                                  allow_redirects=True)
        self.session.headers.update(
            {'X-CSRFToken': login.cookies['csrftoken']})
        self.csrftoken = login.cookies['csrftoken']
        time.sleep(2 * random.random())

        if login.status_code == 200:
            r = self.session.get('https://www.instagram.com/')
            finder = r.text.find(self.user_login)
            if finder != -1:
                self.login_status = True
            else:
                self.login_status = False
                print("Can't login: Invalid login or password.")
        else:
            self.login_status = False
            print("Can't login. Status code: %s" % (login.status_code))

    def logout(self):
        ret = self.post(self.url_logout,
                        {'csrfmiddlewaretoken': self.csrftoken})
        if ret:
            self.login_status = False
        return ret

    def like(self, media_id):
        return self.post(self.url_like % (media_id), None)

    def unlike(self, media_id):
        return self.post(self.url_unlike % (media_id), None)

    def comment(self, media_id, comment_text):
        return self.post(self.url_comment % (media_id),
                         {'comment_text': comment_text})

    def follow(self, user_id):
        ''' You can pass username or user_id of person to follow'''
        return self.post(self.url_follow % self.convert_to_id(user_id), None)

    def unfollow(self, user_id):
        ''' You can pass username or user_id of person to unfollow'''
        return self.post(self.url_unfollow % self.convert_to_id(user_id), None)

    def post(self, url, data):
        if self.login_status:
            try:
                response = self.session.post(url, data=data)
                return response
            except RequestException:
                print("Can't send post request to %s" % url)
        return False

    def convert_to_id(self, inp):
        ''' If input is not digit - it is a username.
            So we should convert it to user_id'''
        if type(inp) == str:
            if not inp.isdigit():
                return self.get_user_id_by_username(inp)
        return str(inp)

# Functions from other files

    def get_profile_info(self, username):
        return get_profile_info(self, username)

    def get_following(self, username):
        return get_following(self, username)

    def get_user_id_by_username(self, username):
        return get_user_id_by_username(self, username)

    def get_feed(self, amount):
        return get_feed(self, amount)
