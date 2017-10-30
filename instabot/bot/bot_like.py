from tqdm import tqdm
from . import limits
from . import delay
from ..api import api_db
from random import randint
import time

#todo ignore if own media
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
    if len(medias) == 0:
        self.logger.info("Nothing to like.")
        return 0
    self.logger.info("like_medias: Going to like %d medias." % (len(medias)))
    this_session_total_liked = 0
    for media in tqdm(medias):
        # if reaching the limit break
        if self.like(media['pk']):
            self.logger.info("like_medias: Liked instagram post with id: %d :" % media['pk'])

            api_db.insertBotAction(self.id_campaign, self.web_application_id_user, media['user']['pk'],
                                   media['user']['full_name'], media['user']['username'],
                                   media['user']['profile_pic_url'], media['pk'],
                                   media['image_versions2']['candidates'][0]['url'],
                                   media['code'], bot_operation, bot_operation_value, self.id_log)
            this_session_total_liked = this_session_total_liked + 1
        else:
            self.logger.info("like_medias: ERROR: COULD NOT LIKE POST WITH ID: %s . GOING TO CONTINUE...", media['pk'])

    self.logger.info("like_medias: DONE: Total liked in this session %d medias." % this_session_total_liked)
    self.logger.info("like_medias: DONE: Total liked %d medias." % self.total_liked)
    return this_session_total_liked


def like_timeline(self, amount=None):
    self.logger.info("like_timeline: Liking %s items from timeline feed:" % amount)
    medias = self.get_timeline_medias(amount=amount)
    bot_operation = "like_timeline"
    return self.like_medias(medias[:amount], bot_operation)


def like_user(self, userObject, bot_operation, bot_operation_value=None, amount=2, filtration=True):
    """ Likes last user_id's medias """

    self.logger.info("like_user: Liking user_%s's feed:" % userObject['full_name'])
    medias = self.get_user_medias(userObject['instagram_id_user'], filtration=filtration)
    if not medias:
        self.logger.info(
            "like_user: None medias received: account is closed or medias have been filtered.")
        return False
    return self.like_medias(medias[:amount], bot_operation=bot_operation, bot_operation_value=bot_operation_value)

#TODO check if get medias return lasst user posts
def like_own_followers(self, likesAmount=100):
    nrLikesPerFollower = 1
    followersAmount = likesAmount / nrLikesPerFollower

    batchSize = followersAmount
    followers = []
    securityBreak = 0
    followersResult = 0

    self.logger.info(
        "like_own_followers:Going to retrieve from database %s followers to perform %s likes " % (followersAmount, likesAmount))
    totalFollowersResult = api_db.fetchOne(
        "select count(*) as total_followers from own_followers where id_user=%s order by id asc",
        self.web_application_id_user)

    self.logger.info('like_own_followers:Total own followers in databasse : %s', totalFollowersResult['total_followers'])
    if totalFollowersResult['total_followers']<batchSize:
      self.logger.info("like_own_followers:There are not enough own followers in database to perform %s likes. Going to perform %s likes. " % (batchSize, totalFollowersResult['total_followers']))
      batchSize=totalFollowersResult['total_followers']
      
    sqlLimitFromWhere = randint(0, (totalFollowersResult['total_followers'] - batchSize))

   
    #this while looks reduntant
    while len(followers) < followersAmount and securityBreak < 10 and followersResult != None:
        self.logger.info('like_own_followers: Getting followers from db starting with offset: %s , limit %s' % ( sqlLimitFromWhere, batchSize))
        
        followersResult = api_db.select("select * from own_followers where id_user=%s order by id_user asc limit %s,%s",
                                        self.web_application_id_user, sqlLimitFromWhere, batchSize)

        # nothing left in db
        if len(followersResult) < 1:
            self.logger.info("like_own_followers: Nothing left in database, going to continue !")
            followersResult = None
            break

        filteredFollowers = []
        self.logger.info("like_own_followers: checking followers !")
        for f in followersResult:
            #this might not be useful
            if self.check_user(f) == True:
                filteredFollowers.append(f)

            sleep_time = randint(1, 3)
            self.logger.info("like_own_followers:Sleeping %s seconds" % sleep_time)
            time.sleep(sleep_time)
            
            if (len(followers) + len(filteredFollowers))>followersAmount:
              break

        followers = followers + filteredFollowers

        self.logger.info(
            "like_own_followers: Iteration %s ,received %s followers, after filtration remained %s followers. Total received %s followers" % (
                securityBreak, len(followersResult), len(filteredFollowers), len(followers)))

        securityBreak = securityBreak + 1
        sqlLimitFromWhere = sqlLimitFromWhere + batchSize

    followers = followers[:followersAmount]

    self.logger.info("like_own_followers: Going to start liking %s followers !" % len(followers))

    totalLiked = 0

    for f in followers:

        totalLiked = totalLiked + self.like_user(userObject=f, bot_operation="like_own_followers",
                                                 amount=nrLikesPerFollower)

    self.logger.info('like_own_followers: Total liked %s posts of your own followers !', totalLiked)

    return totalLiked





def like_users(self, user_ids, nlikes=None, filtration=True):
    for user_id in user_ids:
        if not limits.check_if_bot_can_like(self):
            self.logger.info("Out of likes for today.")
            return
        self.like_user(user_id, amount=nlikes, filtration=filtration)


def like_hashtag(self, hashtag, amount=None):
    self.logger.info("like_posts_by_hashtag: Going to like %s media with hashtag #%s." % (amount, hashtag))
    medias = self.get_hashtag_medias(hashtag=hashtag, filtration=True, amount=amount)
    bot_operation = "like_posts_by_hashtag"
    bot_operation_value = hashtag
    return self.like_medias(medias[:amount], bot_operation, bot_operation_value)


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


def like_posts_by_location(self, locationObject, amount):
    self.logger.info("Going to like %s medias from location %s." % (amount, locationObject['location']))
    medias = self.get_location_medias(id_location=locationObject['id_location'], amount=amount)
    bot_operation = "like_posts_by_location"
    bot_operation_value = locationObject['location']
    return self.like_medias(medias[:amount], bot_operation, bot_operation_value)


def like_other_users_followers(self, userObject, amount):

    self.logger.info('like_other_users_followers: Going to like %s followers of user: %s' % (amount, userObject['username']))

    self.crawl_other_user_followers(userObject=userObject, amount=500)
    
    totalFollowersResult = api_db.fetchOne("select count(*) as total_followers from instagram_user_followers  where fk=%s order by id asc", userObject['id'])

    self.logger.info('like_other_users_followers: Total followers in  database: %s', totalFollowersResult['total_followers'])
    
    batchSize=amount*3
    sqlLimitFromWhere = randint(0, (totalFollowersResult['total_followers'] - batchSize))

    self.logger.info('like_other_users_followers: Getting followers from DATABASE starting with offset: %s, limit %s' % ( sqlLimitFromWhere, batchSize))
    query="select iuf.*, id_campaign from instagram_user_followers iuf " \
          "join instagram_users on (iuf.fk=instagram_users.id) " \
          "join campaign_config on (instagram_users.id_config=campaign_config.id_config) " \
          "where instagram_users.username=%s " \
          "limit %s,%s"

    followers = api_db.select(query, userObject['username'], sqlLimitFromWhere, batchSize)

    self.logger.info('like_other_users_followers: Received from database %s followers of user: %s' % (len(followers),userObject['username']))
  

    if len(followers) == 0:
        self.logger.info("like_other_users_followers: No followers received for user: %s ! SKIPPING" % userObject['username'])
        return 0

    iteration = 0
    securityBreak = 0
    filteredFollowers=[]
    
    
    # check if this follower is valid -> this might not be required / usefull ass it takes alot of time to perform the check
    self.logger.info("like_other_users_followers: Going to check users")

    while len(filteredFollowers) < amount and securityBreak < 400 and len(followers)>iteration+1:
     
      iteration = iteration + 1
      securityBreak = securityBreak + 1

      follower = followers[iteration]
    
      
      if self.check_user(follower) == True:
        filteredFollowers.append(follower)

      sleep_time = randint(1, 3)
      self.logger.info("like_other_users_followers: Sleeping %s seconds" % sleep_time)
      time.sleep(sleep_time)
      self.logger.info("like_other_users_followers: Current followers %s, iteration %s" % ( len(filteredFollowers), securityBreak))

    self.logger.info("like_other_users_followers: Total received %s FILTERED followers" % len(filteredFollowers))
    filteredFollowers = filteredFollowers[:amount]

    totalLiked = 0
  
    for f in filteredFollowers:
        totalLiked = totalLiked + self.like_user(userObject=f, bot_operation="like_other_users_followers",bot_operation_value=userObject['username'],amount=1)

    self.logger.info('like_other_users_followers: Total liked %s posts of %s followers!' % (totalLiked, userObject['username']))

    return totalLiked
