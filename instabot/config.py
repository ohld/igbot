"""
Configuration file of the project
"""

USER_AGENT = """Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36
(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36"""
ACCEPT_LANGUAGE = "ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4"
BASE_COOKIE = {'sessionid': '', 'mid': '', 'ig_pr': '1', 'ig_vw': '1920',
               'csrftoken': '', 's_network': '', 'ds_user_id': ''}
BASE_HEADER = {'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': ACCEPT_LANGUAGE,
               'Connection': 'keep-alive',
               'Content-Length': '0',
               'Host': 'www.instagram.com',
               'Origin': 'https://www.instagram.com',
               'Referer': 'https://www.instagram.com/',
               'User-Agent': USER_AGENT,
               'X-Instagram-AJAX': '1',
               'X-Requested-With': 'XMLHttpRequest'}
