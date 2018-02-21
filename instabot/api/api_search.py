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


def searchLocation(self, query, lat=None, lng=None):
    self.logger.info("searchLocation: Going to search for %s", query)
    self.SendRequest(
        'fbsearch/places/?rank_token=' + str(self.rank_token) + '&query=' + str(query) + '&lat=' + str(
            lat) + '&lng=' + str(lng))
    if not self.LastJson['items']:
        self.logger.info("searchLocation: Did not find any locations using %s query.", query)
        return False
    else:
        self.logger.info("searchLocation: Found %s items.", len(self.LastJson['items']))
        return self.LastJson['items']
