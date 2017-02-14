import time
import random

def like(bot, media_id):
    if not bot.check_media(media_id):
        return False
    if super(bot.__class__, bot).like(media_id):
        bot.total_liked += 1
        return True
    return False

def like_medias(self, medias):
    """ medias - list of ["pk"] fields of response """
    self.logger.info("    Going to like %d medias." % (len(medias)))
    total_liked = 0
    for media in tqdm(medias):
        if self.like(media):
            total_liked += 1
        else:
            pass
        time.sleep(10 * random.random())
    self.logger.info("    DONE: Total liked %d medias. " % total_liked)
    return True

def like_timeline(bot, amount=None):
    """ Likes last 8 medias from timeline feed """
    bot.logger.info("Liking timeline feed:")
    medias = bot.get_timeline_medias()[:amount]
    return bot.like_medias(medias)

def like_user_id(bot, user_id, amount=None):
    """ Likes last user_id's medias """
    if not user_id:
        return False
    bot.logger.info("Liking user_%s's feed:" % user_id)
    medias = bot.get_user_medias(user_id)
    if not medias:
        bot.logger.info("  Can't like user: account is closed!")
        return False
    return bot.like_medias(medias[:amount])

def like_hashtag(bot, hashtag, amount=None):
    """ Likes last medias from hashtag """
    bot.logger.info("Going to like media with hashtag #%s" % hashtag)
    medias = bot.get_hashtag_medias(hashtag)
    return bot.like_medias(medias[:amount])
