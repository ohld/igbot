from . import config


def fbUserSearch(self, query):
    query = self.SendRequest('fbsearch/topsearch/?context=blended&query=' +
                             str(query) + '&rank_token=' + str(self.rank_token))
    return query


def searchUsers(self, query):
    query = self.SendRequest('users/search/?ig_sig_key_version=' + str(config.SIG_KEY_VERSION) +
                             '&is_typeahead=true&query=' + str(query) + '&rank_token=' + str(self.rank_token))
    return query


def searchUsername(self, usernameName):
    query = self.SendRequest('users/' + str(usernameName) + '/usernameinfo/')
    return query


def searchTags(self, query):
    query = self.SendRequest('tags/search/?is_typeahead=true&q=' +
                             str(query) + '&rank_token=' + str(self.rank_token))
    return query


def searchLocation(self, query):
    locationFeed = self.SendRequest(
        'fbsearch/places/?rank_token=' + str(self.rank_token) + '&query=' + str(query))
    return locationFeed
