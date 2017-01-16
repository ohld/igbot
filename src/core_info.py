import requests
import json
import time, datetime
import random
import sys
from tqdm import tqdm

def get_user_id_by_username(self, username):
    url_info= self.url_user_info % (username)
    info = self.s.get(url_info)
    all_data = json.loads(info.text)
    id_user = all_data['user']['id']
    return id_user

def get_followers(self, username):
    print ("Getting followers of %s"%username)
    userid = self.get_user_id_by_username(username)
    response = self.post('https://www.instagram.com/query/', {
        'q': '''ig_user(%s) {
              follows.first(20) {
                count,
                page_info {
                  end_cursor, has_next_page
                },
                nodes {
                  id, is_verified, full_name, username
                }
              }
        }'''%(userid),
      'ref': 'relationships::follow_list',
      'query_id': '%d'%random.randint(0, 99999999999)
    })

    if response.status_code != 200:
        return False
    data = response.json()
    persons = data["follows"]["nodes"]
    total_follows = data["follows"]["count"]
    with tqdm(total=total_follows) as pbar:
        pbar.update(len(persons))
        while data["follows"]["page_info"]["has_next_page"]:
            time.sleep(3 * random.random())
            cursor = data["follows"]["page_info"]["end_cursor"]
            response = self.post('https://www.instagram.com/query/', {
                'q': '''ig_user(%s) {
                      follows.after(%s, 20) {
                        count,
                        page_info {
                          end_cursor, has_next_page
                        },
                        nodes {
                          id, is_verified, full_name, username
                        }
                      }
                }'''%(userid, cursor),
              'ref': 'relationships::follow_list',
              'query_id': '%d'%random.randint(0, 99999999999)
            })

            if response.status_code != 200:
                print ("Error while requesting more followers")
                return persons
            data = response.json()
            pbar.update(len(data["follows"]["nodes"]))
            persons.extend(data["follows"]["nodes"])
    return persons

def get_profile_info (self, username):
        if (self.login_status):
            now_time = datetime.datetime.now()
            if self.login_status == 1:
                url = 'https://www.instagram.com/%s/'%(username)
                try :
                    r = self.s.get(url)
                    text = r.text
                    finder_text_start = ('<script type="text/javascript">'
                                             'window._sharedData = ')
                    finder_text_start_len = len(finder_text_start)-1
                    finder_text_end = ';</script>'

                    all_data_start = text.find(finder_text_start)
                    all_data_end = text.find(finder_text_end, all_data_start + 1)
                    json_str = text[(all_data_start + finder_text_start_len + 1) \
                                       : all_data_end]
                    all_data = json.loads(json_str)
                    user_info = list(all_data['entry_data']['ProfilePage'])
                    user_id = user_info[0]['user']['id']
                    is_verified = user_info[0]['user']['is_verified']
                    follows = user_info[0]['user']['follows']['count']
                    followed_by = user_info[0]['user']['followed_by']['count']

                    media = user_info[0]['user']['media']['count']
                    follows_viewer = user_info[0]['user']['follows_viewer']
                    followed_by_viewer = user_info[0]['user']['followed_by_viewer']
                    requested_by_viewer = user_info[0]['user']['requested_by_viewer']
                    has_requested_viewer = user_info[0]['user']['has_requested_viewer']
                    return {
                        "date":now_time.strftime("%d.%m.%Y %H:%M"),
                        "id": user_id,
                        "is_verified": is_verified,
                        "media": media,
                        "follows": follows,
                        "followed_by": followed_by,
                        "follows_viewer": follows_viewer,
                        "followed_by_viewer": followed_by_viewer,
                        "requested_by_viewer": requested_by_viewer,
                        "has_requested_viewer": has_requested_viewer
                    }

                except:
                    return False
            else:
                return False
