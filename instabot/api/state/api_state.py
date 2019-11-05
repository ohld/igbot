from instaprole.utils.generic_utils.singleton import Singleton


class API_State(metaclass=Singleton):

    def __init__(self):
        self.total_requests = 0

    def __repr__(self):
        return self.__dict__
