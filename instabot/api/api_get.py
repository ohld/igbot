from __future__ import unicode_literals

import requests


def get_user_id_from_username(self, username):
    try:
        response = requests.get('https://www.instagram.com/' + username + '/?__a=1')
        if response.status_code == 200:
            response_body = response.json()
            return response_body["graphql"]["user"]["id"]
    except KeyError as e:
        self.logger.error("API.GET - Get user id from username {} failed.".format(username))
        raise e
