import os
import hmac
import pickle
import warnings
import json

from enum import IntEnum

from . import config


class Dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    __repr__ = dict.__repr__
    def __str__(self):
        s = ""
        for key, value in self.items():
            s += "%s: %s\n" % (str(key), str(value))
        return s
    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)


class User(object):
    """ Class to store all user's properties """

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.api_is_set = False
        self.bot_is_set = False
        self.isLoggedIn = False
        self.counters = Dotdict({})
        self.limits = Dotdict({})
        self.delays = Dotdict({})
        self.filters = Dotdict({})

    def save(self):
        if not os.path.exists(config.USERS_FOLDER_NAME):
            os.makedirs(config.USERS_FOLDER_NAME)
        output_path = config.USERS_FOLDER_NAME + "%s.user" % self.username
        with open(output_path, 'wb') as foutput:
            pickle.dump(self, foutput)

    @classmethod
    def load(cls, username):
        input_path = config.USERS_FOLDER_NAME + "%s.user" % username
        if os.path.exists(input_path):
            with open(input_path, 'rb') as finput:
                return pickle.load(finput)
        else:
            warnings.warn("No user found")
            return None

    @staticmethod
    def delete(username):
        input_path = config.USERS_FOLDER_NAME + "%s.user" % username
        if os.path.exists(input_path):
            os.remove(input_path)

    def dump(self):
        items = self.__dict__.copy()
        # del items["counters"]
        return json.dumps(items, indent=2)
