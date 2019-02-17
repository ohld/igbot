from .. import utils


def whitelist(self):
    return utils.file(self.username + '_whitelist.txt')


def blacklist(self):
    return utils.file(self.username + '_blacklist.txt')


def comments(self):
    return utils.file(self.username + '_comments.txt')


def followed(self):
    return utils.file(self.username + '_followed.txt')


def unfollowed(self):
    return utils.file(self.username + '_unfollowed.txt')


def skipped(self):
    return utils.file(self.username + '_skipped.txt')


def friends(self):
    return utils.file(self.username + '_friends.txt')
