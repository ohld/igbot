from tqdm import tqdm

from . import limits
from . import delay


def block(self, user_id):
    user_id = self.convert_to_user_id(user_id)
    if self.check_not_bot(user_id):
        return True
    if limits.check_if_bot_can_block(self):
        delay.block_delay(self)
        if super(self.__class__, self).block(user_id):
            self.total_blocked += 1
            return True
    else:
        self.logger.info("Out of blocks for today.")
    return False


def unblock(self, user_id):
    user_id = self.convert_to_user_id(user_id)
    if limits.check_if_bot_can_unblock(self):
        delay.unblock_delay(self)
        if super(self.__class__, self).unblock(user_id):
            self.total_unblocked += 1
            return True
    else:
        self.logger.info("Out of blocks for today.")
    return False


def block_users(self, user_ids):
    broken_items = []
    self.logger.info("Going to block %d users." % len(user_ids))
    for user_id in tqdm(user_ids):
        if not self.block(user_id):
            delay.error_delay(self)
            broken_items.append(user_id)
    self.logger.info("DONE: Total blocked %d users." % self.total_blocked)
    return broken_items


def unblock_users(self, user_ids):
    broken_items = []
    self.logger.info("Going to unblock %d users." % len(user_ids))
    for user_id in tqdm(user_ids):
        if not self.unblock(user_id):
            delay.error_delay(self)
            broken_items.append(user_id)
    self.logger.info("DONE: Total unblocked %d users." % self.total_unblocked)
    return broken_items
