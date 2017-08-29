from tqdm import tqdm
from . import limits
from . import delay
from ..api import api_db


def like(self, media_id):
    if limits.check_if_bot_can_like(self):
        delay.like_delay(self)
        if super(self.__class__, self).like(media_id):
            self.total_liked += 1
            return True
    else:
        self.logger.info("Out of likes for today.")
    return False


def like_medias(self, medias, bot_operation=None, bot_operation_value=None):
    broken_items = []
    if len(medias) == 0:
        self.logger.info("Nothing to like.")
        return broken_items
    self.logger.info("Going to like %d medias." % (len(medias)))
    this_session_total_liked=0
    for media in tqdm(medias):
        #if reaching the limit break
        if not self.like(media['pk']):
            delay.error_delay(self)
            broken_items.append(media)
            break
        self.logger.info("Liked instagram post with id: %d :" % media['pk'])

        api_db.insert("insert into likes (id_campaign,id_user,username,full_name,instagram_id_user,code,id_post,image,bot_operation,bot_operation_value) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                      self.id_campaign, self.id_user, media['user']['username'],media['user']['full_name'],media['user']['pk'],
                      media['code'],media['pk'],media['image_versions2']['candidates'][0]['url'],bot_operation, bot_operation_value)
        this_session_total_liked=this_session_total_liked+1

    self.logger.info("DONE: Total liked in this session %d medias." % this_session_total_liked)
    self.logger.info("DONE: Total liked %d medias." % self.total_liked)
    return broken_items


def like_timeline(self, amount=None):
    self.logger.info("Liking %s items from timeline feed:" % amount)
    medias = self.get_timeline_medias(amount=amount)
    bot_operation="like_timeline"
    return self.like_medias(medias,bot_operation)


def like_user(self, user_id, amount=None, filtration=True):
    """ Likes last user_id's medias """
    if filtration:
        if not self.check_user(user_id, filter_closed_acc=True):
            return False
    self.logger.info("Liking user_%s's feed:" % user_id)
    user_id = self.convert_to_user_id(user_id)
    medias = self.get_user_medias(user_id, filtration=filtration)
    if not medias:
        self.logger.info(
            "None medias received: account is closed or medias have been filtered.")
        return False
    return self.like_medias(medias[:amount])


def like_users(self, user_ids, nlikes=None, filtration=True):
    for user_id in user_ids:
        if not limits.check_if_bot_can_like(self):
            self.logger.info("Out of likes for today.")
            return
        self.like_user(user_id, amount=nlikes, filtration=filtration)


def like_hashtag(self, hashtag, amount=None):
    """ Likes last medias from hashtag """
    self.logger.info("Amount is %s" % amount)
    self.logger.info("Going to like media with hashtag #%s." % hashtag)
    medias = self.get_hashtag_medias(hashtag=hashtag, filtration=True, amount=amount)
    bot_operation="like_posts_by_hashtag"
    bot_operation_value = hashtag
    return self.like_medias(medias[:amount],bot_operation, bot_operation_value)


def like_geotag(self, geotag, amount=None):
    # TODO: like medias by geotag
    pass


def like_followers(self, user_id, nlikes=None):
    self.logger.info("Like followers of: %s." % user_id)
    if not limits.check_if_bot_can_like(self):
        self.logger.info("Out of likes for today.")
        return
    if not user_id:
        self.logger.info("User not found.")
        return
    follower_ids = self.get_user_followers(user_id)
    if not follower_ids:
        self.logger.info("%s not found / closed / has no followers." % user_id)
    else:
        self.like_users(follower_ids, nlikes)


def like_following(self, user_id, nlikes=None):
    self.logger.info("Like following of: %s." % user_id)
    if not limits.check_if_bot_can_like(self):
        self.logger.info("Out of likes for today.")
        return
    if not user_id:
        self.logger.info("User not found.")
        return
    following_ids = self.get_user_following(user_id)
    if not following_ids:
        self.logger.info("%s not found / closed / has no following." % user_id)
    else:
        self.like_users(following_ids, nlikes)
        
def like_posts_by_location(self, id_location, amount):
    self.logger.info("Going to like %s medias from location %s." % (amount,id_location))
    medias = self.get_location_medias(id_location=id_location, amount=amount)
    bot_operation="like_posts_by_location"
    bot_operation_value=id_location
    return self.like_medias(medias[:amount],bot_operation,bot_operation_value)
    
   
   
