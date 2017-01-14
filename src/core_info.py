import requests
import json
import time, random

def get_user_id_by_username(self, username):
    url_info= self.url_user_info % (username)
    info = self.s.get(url_info)
    all_data = json.loads(info.text)
    id_user = all_data['user']['id']
    return id_user

def get_followers(self, username):
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
        persons.extend(data["follows"]["nodes"])
    return persons

# curl 'https://www.instagram.com/query/' \
# -XPOST \
# -H 'Content-Type: application/x-www-form-urlencoded' \
# -H 'Referer: https://www.instagram.com/ohld/following/' \
# -H 'Accept: */*' \
# -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14' \
# -H 'Origin: https://www.instagram.com' \
# -H 'X-Instagram-AJAX: 1' \
# -H 'X-CSRFToken: 5Q5RIUzHTih1QxvMIO1tVjaXB6Xf2yhN' \
# -H 'X-Requested-With: XMLHttpRequest' \
# --data 'q=ig_user(352300017)+%7B%0A++follows.after(AQBrKskTD0YqJSweCPf9ee3ITIyfgS3RXiyVtKCJ6ySkgAS11WF_4kAOvPgEvAFUNcd382zcG2d07RkCkBQi9NcUQTkQAVoWC8-fhsBUPHsL9HgQ1Yyg4HrxGD_1uLPQpA0%2C+10)+%7B%0A++++count%2C%0A++++page_info+%7B%0A++++++end_cursor%2C%0A++++++has_next_page%0A++++%7D%2C%0A++++nodes+%7B%0A++++++id%2C%0A++++++is_verified%2C%0A++++++followed_by_viewer%2C%0A++++++requested_by_viewer%2C%0A++++++full_name%2C%0A++++++profile_pic_url%2C%0A++++++username%0A++++%7D%0A++%7D%0A%7D%0A&ref=relationships%3A%3Afollow_list&query_id=17867281162062470'


# curl 'https://www.instagram.com/query/' \
# -XPOST \
# -H 'Content-Type: application/x-www-form-urlencoded' \
# -H 'Referer: https://www.instagram.com/ohld/' \
# -H 'Accept: */*' \
# -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14' \
# -H 'Origin: https://www.instagram.com' \
# -H 'X-Instagram-AJAX: 1' \
# -H 'X-CSRFToken: 5Q5RIUzHTih1QxvMIO1tVjaXB6Xf2yhN' \
# -H 'X-Requested-With: XMLHttpRequest' \
# --data 'q=ig_user(352300017)+%7B%0A++follows.first(10)+%7B%0A++++count%2C%0A++++page_info+%7B%0A++++++end_cursor%2C%0A++++++has_next_page%0A++++%7D%2C%0A++++nodes+%7B%0A++++++id%2C%0A++++++is_verified%2C%0A++++++followed_by_viewer%2C%0A++++++requested_by_viewer%2C%0A++++++full_name%2C%0A++++++profile_pic_url%2C%0A++++++username%0A++++%7D%0A++%7D%0A%7D%0A&ref=relationships%3A%3Afollow_list&query_id=17867281162062470'
