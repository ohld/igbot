from . import config


def fbUserSearch(self, query):
    url = 'fbsearch/topsearch/?context=blended&query={query}&rank_token={rank_token}'.format(
        query=query,
        rank_token=self.rank_token
    )
    return self.SendRequest(url)


def searchUsers(self, query):
    url = 'users/search/?ig_sig_key_version={sig_key}&is_typeahead=true&query={query}&rank_token={rank_token}'.format(
        sig_key=config.SIG_KEY_VERSION,
        query=query,
        rank_token=self.rank_token
    )
    return self.SendRequest(url)


def searchUsername(self, usernameName):
    query = self.SendRequest('users/' + str(usernameName) + '/usernameinfo/')
    return query


def searchTags(self, query):
    url = 'tags/search/?is_typeahead=true&q={query}&rank_token={rank_token}'.format(
        query=query,
        rank_token=self.rank_token
    )
    return self.SendRequest(url)


def searchLocation(self, query, lat=None, lng=None):
    locationFeed = self.SendRequest(
        'fbsearch/places/?rank_token=' + str(self.rank_token) + '&query=' + str(query) + '&lat=' + str(lat) + '&lng=' + str(lng))
    return locationFeed
