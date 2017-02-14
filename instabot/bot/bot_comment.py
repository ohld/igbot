"""
    Bot functions to generate and post a comments.

    Instructions to file with comments:
        one line - one comment.

    Example:
        lol
        kek

"""

import random
import os
import io

def comment_hashtag(bot, hashtag, amount=None):
    bot.logger.info("Going to comment medias by %s hashtag" % hashtag)
    medias = bot.get_hashtag_medias(hashtag)
    return bot.comment_medias(medias[:amount])

def get_random_comment_from_file(file_path):
    with io.open(file_path, "r", encoding="utf8") as f:
        content = f.readlines()
        return random.choice(content).strip()

def get_comment(bot, comment_base_file=None):
    """
        Generates comment.
        If comment_base_file argunment is passed, it uses the lines from file
        as comments to return.

        TODO: generate more ways to create comments.
    """
    if comment_base_file is not None:
        if os.path.exists(comment_base_file):
            return get_random_comment_from_file(comment_base_file)
        else:
            bot.logger.info("Can't find your file with comments.")
            return "lol"
    else:
        return "lol"

def is_commented(bot, media_id):
    """
    checks if media is already commented
    """
    bot.getMediaComments(media_id)
    # print (bot.LastJson)
    if 'comments' not in bot.LastJson:
        return False
    usernames = [item["user"]["username"] for item in bot.LastJson['comments']]
    return bot.username in usernames

def comment_medias(self, medias):
    """ medias - list of ["pk"] fields of response """
    self.logger.info("    Going to comment on %d medias." % (len(medias)))
    total_commented = 0
    for media in tqdm(medias):

        # grab a comment
        co = self.get_comment('comments.txt')

        if self.comment(media, co):
            total_commented += 1
        else:
            pass
        time.sleep(10 * random.random())
    self.logger.info("    DONE: Total commented on %d medias. " % total_commented)
    return True

def comment_users(bot, user_ids):
    """ Put a comment to last media of every user from list"""
    pass
