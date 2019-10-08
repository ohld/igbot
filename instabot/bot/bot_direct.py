import os
from mimetypes import guess_type

from tqdm import tqdm


def send_message(self, text, user_ids, thread_id=None):
    """
    :param self: bot
    :param text: text of message
    :param user_ids: list of user_ids for creating group or
    one user_id for send to one person
    :param thread_id: thread_id
    """
    user_ids = _get_user_ids(self, user_ids)
    if not isinstance(text, str) and isinstance(user_ids, (list, str)):
        self.logger.error(
            "Text must be an string, user_ids must be an list or string"
        )
        return False

    if self.reached_limit("messages"):
        self.logger.info("Out of messages for today.")
        return False

    self.delay("message")
    urls = self.extract_urls(text)
    item_type = "link" if urls else "text"
    if self.api.send_direct_item(
        item_type, user_ids, text=text, thread=thread_id, urls=urls
    ):
        self.total["messages"] += 1
        return True

    self.logger.info("Message to {user_ids} wasn't sent".format(
        user_ids=user_ids)
    )
    return False


def send_messages(self, text, user_ids):
    broken_items = []
    if not user_ids:
        self.logger.info("User must be at least one.")
        return broken_items
    self.logger.info("Going to send %d messages." % (len(user_ids)))
    for user in tqdm(user_ids):
        if not self.send_message(text, user):
            self.error_delay()
            broken_items = user_ids[user_ids.index(user):]
            break
    return broken_items


def send_media(self, media_id, user_ids, text="", thread_id=None):
    """
    :param media_id:
    :param self: bot
    :param text: text of message
    :param user_ids: list of user_ids for creating group or one user_id
    for send to one person
    :param thread_id: thread_id
    """
    user_ids = _get_user_ids(self, user_ids)
    if not isinstance(text, str) and not isinstance(user_ids, (list, str)):
        self.logger.error(
            "Text must be an string, user_ids must be an list or string"
        )
        return False
    if self.reached_limit("messages"):
        self.logger.info("Out of messages for today.")
        return False

    media = self.get_media_info(media_id)
    media = media[0] if isinstance(media, list) else media

    self.delay("message")
    if self.api.send_direct_item(
        "media_share",
        user_ids,
        text=text,
        thread=thread_id,
        media_type=media.get("media_type"),
        media_id=media.get("id"),
    ):
        self.total["messages"] += 1
        return True

    self.logger.info("Message to {user_ids} wasn't sent".format(
        user_ids=user_ids)
    )
    return False


def send_medias(self, media_id, user_ids, text):
    broken_items = []
    if not user_ids:
        self.logger.info("User must be at least one.")
        return broken_items
    self.logger.info("Going to send %d messages." % (len(user_ids)))
    for user in tqdm(user_ids):
        if not self.send_media(media_id, user, text):
            self.error_delay()
            broken_items = user_ids[user_ids.index(user):]
            break
    return broken_items


def send_hashtag(self, hashtag, user_ids, text="", thread_id=None):
    """
    :param hashtag: hashtag
    :param self: bot
    :param text: text of message
    :param user_ids: list of user_ids for creating group or one
    user_id for send to one person
    :param thread_id: thread_id
    """
    user_ids = _get_user_ids(self, user_ids)
    if not isinstance(text, str) and not isinstance(user_ids, (list, str)):
        self.logger.error(
            "Text must be an string, user_ids must be an list or string"
        )
        return False

    if self.reached_limit("messages"):
        self.logger.info("Out of messages for today.")
        return False

    self.delay("message")
    if self.api.send_direct_item(
        "hashtag", user_ids, text=text, thread=thread_id, hashtag=hashtag
    ):
        self.total["messages"] += 1
        return True

    self.logger.info("Message to {user_ids} wasn't sent".format(
        user_ids=user_ids)
    )
    return False


def send_profile(self, profile_user_id, user_ids, text="", thread_id=None):
    """
    :param profile_user_id: profile_id
    :param self: bot
    :param text: text of message
    :param user_ids: list of user_ids for creating group or
    one user_id for send to one person
    :param thread_id: thread_id
    """
    profile_id = self.convert_to_user_id(profile_user_id)
    user_ids = _get_user_ids(self, user_ids)
    if not isinstance(text, str) and not isinstance(user_ids, (list, str)):
        self.logger.error(
            "Text must be an string, user_ids must be an list or string"
        )
        return False

    if self.reached_limit("messages"):
        self.logger.info("Out of messages for today.")
        return False

    self.delay("message")
    if self.api.send_direct_item(
        "profile",
        user_ids,
        text=text,
        thread=thread_id,
        profile_user_id=profile_id
    ):
        self.total["messages"] += 1
        return True
    self.logger.info("Message to {user_ids} wasn't sent".format(
        user_ids=user_ids)
    )
    return False


def send_like(self, user_ids, thread_id=None):
    """
    :param self: bot
    :param user_ids: list of user_ids for creating group or
    one user_id for send to one person
    :param thread_id: thread_id
    """
    user_ids = _get_user_ids(self, user_ids)
    if not isinstance(user_ids, (list, str)):
        self.logger.error(
            "Text must be an string, user_ids must be an list or string"
        )
        return False

    if self.reached_limit("messages"):
        self.logger.info("Out of messages for today.")
        return False

    self.delay("message")
    if self.api.send_direct_item("like", user_ids, thread=thread_id):
        self.total["messages"] += 1
        return True
    self.logger.info("Message to {user_ids} wasn't sent".format(
        user_ids=user_ids)
    )
    return False


def send_photo(self, user_ids, filepath, thread_id=None):
    """
    :param self: bot
    :param filepath: file path to send
    :param user_ids: list of user_ids for creating group or
    one user_id for send to one person
    :param thread_id: thread_id
    """
    user_ids = _get_user_ids(self, user_ids)
    if not isinstance(user_ids, (list, str)):
        self.logger.error("user_ids must be a list or string")
        return False

    if self.reached_limit("messages"):
        self.logger.info("Out of messages for today.")
        return False

    if not os.path.exists(filepath):
        self.logger.error("File %s is not found", filepath)
        return False

    mime_type = guess_type(filepath)
    if mime_type[0] != "image/jpeg":
        self.logger.error("Only jpeg files are supported")
        return False

    self.delay("message")
    if not self.api.send_direct_item(
        "photo", user_ids, filepath=filepath, thread=thread_id
    ):
        self.logger.info("Message to %s wasn't sent", user_ids)
        return False

    self.total["messages"] += 1
    return True


def _get_user_ids(self, user_ids):
    if isinstance(user_ids, str):
        user_ids = self.convert_to_user_id(user_ids)
        return [user_ids]
    return [self.convert_to_user_id(user) for user in user_ids]


def approve_pending_thread_requests(self):
    pending = self.get_pending_thread_requests()
    if pending:
        for thread in pending:
            thread_id = thread["thread_id"]
            self.api.approve_pending_thread(thread_id)
            if self.api.last_response.status_code == 200:
                self.logger.info("Approved thread: {}".format(thread_id))
            else:
                self.logger.error(
                    "Could not approve thread {}".format(thread_id)
                )
