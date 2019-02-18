from .. import utils


def set_whitelist(self):
    if self.default_files:
        return utils.file('whitelist.txt')
    else:
        return utils.file(self.username + '_whitelist.txt')


def set_blacklist(self):
    if self.default_files:
        return utils.file('blacklist.txt')
    else:
        return utils.file(self.username + '_blacklist.txt')


def set_comments(self):
    if self.default_files:
        return utils.file('comments.txt')
    else:
        return utils.file(self.username + '_comments.txt')


def set_followed(self):
    if self.default_files:
        return utils.file('followed.txt')
    else:
        return utils.file(self.username + '_followed.txt')


def set_unfollowed(self):
    if self.default_files:
        return utils.file('unfollowed.txt')
    else:
        return utils.file(self.username + '_unfollowed.txt')


def set_skipped(self):
    if self.default_files:
        return utils.file('skipped.txt')
    else:
        return utils.file(self.username + '_skipped.txt')


def set_friends(self):
    if self.default_files:
        return utils.file('friends.txt')
    else:
        return utils.file(self.username + '_friends.txt')
