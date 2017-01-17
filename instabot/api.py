import requests, json
import time, random

from api_info import *
from prepare import get_credentials

class API:

    user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
    accept_language = 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
    url            = 'https://www.instagram.com/'
    url_tag        = 'https://www.instagram.com/explore/tags/'
    url_like       = 'https://www.instagram.com/web/likes/%s/like/'
    url_unlike     = 'https://www.instagram.com/web/likes/%s/unlike/'
    url_comment    = 'https://www.instagram.com/web/comments/%s/add/'
    url_follow     = 'https://www.instagram.com/web/friendships/%s/follow/'
    url_unfollow   = 'https://www.instagram.com/web/friendships/%s/unfollow/'
    url_login      = 'https://www.instagram.com/accounts/login/ajax/'
    url_logout     = 'https://www.instagram.com/accounts/logout/'
    url_media_info = 'https://www.instagram.com/p/%s/?__a=1'
    url_user_info  = 'https://www.instagram.com/%s/?__a=1'

    def __init__(self):
        login, password = get_credentials()
        self.user_login = login.lower()
        self.user_password = password
        self.s = requests.Session()

        self.login()

    def login(self):
        self.s.cookies.update({'sessionid': '', 'mid': '', 'ig_pr': '1',
                               'ig_vw': '1920', 'csrftoken': '',
                               's_network': '', 'ds_user_id': ''})
        self.login_post = {'username': self.user_login,
                           'password': self.user_password}
        self.s.headers.update({'Accept-Encoding': 'gzip, deflate',
                               'Accept-Language': self.accept_language,
                               'Connection': 'keep-alive',
                               'Content-Length': '0',
                               'Host': 'www.instagram.com',
                               'Origin': 'https://www.instagram.com',
                               'Referer': 'https://www.instagram.com/',
                               'User-Agent': self.user_agent,
                               'X-Instagram-AJAX': '1',
                               'X-Requested-With': 'XMLHttpRequest'})
        r = self.s.get(self.url)
        self.s.headers.update({'X-CSRFToken': r.cookies['csrftoken']})
        time.sleep(2 * random.random())
        login = self.s.post(self.url_login, data=self.login_post,
                            allow_redirects=True)
        self.s.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
        self.csrftoken = login.cookies['csrftoken']
        time.sleep(2 * random.random())

        if login.status_code == 200:
            r = self.s.get('https://www.instagram.com/')
            finder = r.text.find(self.user_login)
            if finder != -1:
                self.login_status = True
            else:
                self.login_status = False
                print ("Can't login: Invalid login or password.")
        else:
            self.login_status = False
            print ("Can't login. Status code: %s"%(login.status_code))

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
        return self.post(self.url_follow % (user_id), None)

    def unfollow(self, user_id):
        return self.post(self.url_unfollow % (user_id), None)

    def post(self, url, data):
        if (self.login_status):
            try:
                response = self.s.post(url, data=data)
                return response
            except:
                print ("Can't send post request to %s"%url)
                pass
        return False

###### Finctions from other files ######

    def get_profile_info(self, username):
        return get_profile_info(self, username)

    def get_followers(self, username):
        return get_followers(self, username)

    def get_user_id_by_username(self, username):
        return get_user_id_by_username(self, username)
