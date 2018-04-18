from . import config


def fb_user_search(self, query):
    url = 'fbsearch/topsearch/?context=blended&query={query}&rank_token={rank_token}'.format(
        query=query,
        rank_token=self.rank_token
    )
    return self.send_request(url)


def search_users(self, query):
    url = 'users/search/?ig_sig_key_version={sig_key}&is_typeahead=true&query={query}&rank_token={rank_token}'.format(
        sig_key=config.SIG_KEY_VERSION,
        query=query,
        rank_token=self.rank_token
    )
    return self.send_request(url)


def search_username(self, usernameName):
    query = self.send_request('users/' + str(usernameName) + '/usernameinfo/')
    return query


def search_tags(self, query):
    url = 'tags/search/?is_typeahead=true&q={query}&rank_token={rank_token}'.format(
        query=query,
        rank_token=self.rank_token
    )
    return self.send_request(url)


def search_location(self, query, lat=None, lng=None):
    locationFeed = self.send_request(
        'fbsearch/places/?rank_token=' + str(self.rank_token) + '&query=' + str(query) + '&lat=' + str(lat) + '&lng=' + str(lng))
    return locationFeed
