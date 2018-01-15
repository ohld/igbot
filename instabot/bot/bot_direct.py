from tqdm import tqdm

from . import delay


def send_message(self, text, user_ids, thread_id=None):
    """
    :param self: bot
    :param text: text of message
    :param user_ids: list of user_ids for creating group or one user_id for send to one person
    :param thread_id: thread_id
    """
    user_ids = _get_user_ids(self, user_ids)
    if not isinstance(text, str) and isinstance(user_ids, (list, str)):
        self.logger.error('Text must be an string, user_ids must be an list or string')
        return False
    delay.small_delay(self)
    urls = self.extract_urls(text)
    item_type = 'links' if urls else 'message'
    if super(self.__class__, self).sendDirectItem(item_type, user_ids, text=text,
                                                  thread=thread_id, urls=urls):
        # ToDo: need to add counter
        return True
    self.logger.info("Message to {user_ids} wasn't sended".format(user_ids=user_ids))
    return False


def send_messages(self, text, user_ids):
    broken_items = []
    if not user_ids:
        self.logger.info("User must be at least one.")
        return broken_items
    self.logger.info("Going to send %d messages." % (len(user_ids)))
    for user in tqdm(user_ids):
        if not self.send_message(text, user):
            delay.error_delay(self)
            broken_items = user_ids[user_ids.index(user):]
            break
    return broken_items


def send_media(self, media_id, user_ids, text='', thread_id=None):
    """
    :param media_id:
    :param self: bot
    :param text: text of message
    :param user_ids: list of user_ids for creating group or one user_id for send to one person
    :param thread_id: thread_id
    """
    user_ids = _get_user_ids(self, user_ids)
    if not isinstance(text, str) and not isinstance(user_ids, (list, str)):
        self.logger.error('Text must be an string, user_ids must be an list or string')
        return False
    media = self.get_media_info(media_id)
    media = media[0] if isinstance(media, list) else media
    delay.small_delay(self)
    if super(self.__class__, self).sendDirectItem('media_share', user_ids, text=text, thread=thread_id,
                                                  media_type=media.get('media_type'), media_id=media.get('id')):
        # ToDo: need to add counter
        return True
    self.logger.info("Message to {user_ids} wasn't sended".format(user_ids=user_ids))
    return False


def send_medias(self, media_id, user_ids, text):
    broken_items = []
    if not user_ids:
        self.logger.info("User must be at least one.")
        return broken_items
    self.logger.info("Going to send %d messages." % (len(user_ids)))
    for user in tqdm(user_ids):
        if not self.send_media(media_id, user, text):
            delay.error_delay(self)
            broken_items = user_ids[user_ids.index(user):]
            break
    return broken_items


def send_hashtag(self, hashtag, user_ids, text='', thread_id=None):
    """
    :param hashtag: hashtag
    :param self: bot
    :param text: text of message
    :param user_ids: list of user_ids for creating group or one user_id for send to one person
    :param thread_id: thread_id
    """
    user_ids = _get_user_ids(self, user_ids)
    if not isinstance(text, str) and not isinstance(user_ids, (list, str)):
        self.logger.error('Text must be an string, user_ids must be an list or string')
        return False
    delay.small_delay(self)
    if super(self.__class__, self).sendDirectItem('hashtag', user_ids, text=text, thread=thread_id,
                                                  hashtag=hashtag):
        # ToDo: need to add counter
        return True
    self.logger.info("Message to {user_ids} wasn't sended".format(user_ids=user_ids))
    return False


def send_profile(self, profile_user_id, user_ids, text='', thread_id=None):
    """
    :param profile_user_id: profile_id
    :param self: bot
    :param text: text of message
    :param user_ids: list of user_ids for creating group or one user_id for send to one person
    :param thread_id: thread_id
    """
    profile_id = self.convert_to_user_id(profile_user_id)
    user_ids = _get_user_ids(self, user_ids)
    if not isinstance(text, str) and not isinstance(user_ids, (list, str)):
        self.logger.error('Text must be an string, user_ids must be an list or string')
        return False
    delay.small_delay(self)
    if super(self.__class__, self).sendDirectItem('profile', user_ids, text=text, thread=thread_id,
                                                  profile_user_id=profile_id):
        # ToDo: need to add counter
        return True
    self.logger.info("Message to {user_ids} wasn't sended".format(user_ids=user_ids))
    return False


def send_like(self, user_ids, thread_id=None):
    """
    :param self: bot
    :param text: text of message
    :param user_ids: list of user_ids for creating group or one user_id for send to one person
    :param thread_id: thread_id
    """
    user_ids = _get_user_ids(self, user_ids)
    if not isinstance(user_ids, (list, str)):
        self.logger.error('Text must be an string, user_ids must be an list or string')
        return False
    delay.small_delay(self)
    if super(self.__class__, self).sendDirectItem('like', user_ids, thread=thread_id):
        # ToDo: need to add counter
        return True
    self.logger.info("Message to {user_ids} wasn't sended".format(user_ids=user_ids))
    return False


def _get_user_ids(self, user_ids):
    if isinstance(user_ids, str):
        user_ids = self.convert_to_user_id(user_ids)
        return [user_ids]
    return [self.convert_to_user_id(user) for user in user_ids]
