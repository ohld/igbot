from tqdm import tqdm
from . import limits
from . import delay
from ..api import api_db
from random import randint
import time
import json

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
        return 0
    self.logger.info("Going to like %d medias." % (len(medias)))
    this_session_total_liked = 0
    for media in tqdm(medias):
        # if reaching the limit break
        if not self.like(media['pk']):
            delay.error_delay(self)
            broken_items.append(media)
            self.logger.info("ERROR: GOING TO BREAK ! COULD NOT LIKE A POST WITH ID: %s", media['pk'])
            break
        self.logger.info("Liked instagram post with id: %d :" % media['pk'])

        api_db.insertBotAction(self.id_campaign, self.web_application_id_user, media['user']['pk'],
                               media['user']['full_name'], media['user']['username'],
                               media['user']['profile_pic_url'], media['pk'],
                               media['image_versions2']['candidates'][0]['url'],
                               media['code'], bot_operation, bot_operation_value, self.id_log)
        this_session_total_liked = this_session_total_liked + 1

    self.logger.info("DONE: Total liked in this session %d medias." % this_session_total_liked)
    self.logger.info("DONE: Total liked %d medias." % self.total_liked)
    return this_session_total_liked


def like_timeline(self, amount=None):
    self.logger.info("Liking %s items from timeline feed:" % amount)
    medias = self.get_timeline_medias(amount=amount)
    bot_operation = "like_timeline"
    return self.like_medias(medias, bot_operation)


def like_user(self, userObject, bot_operation, bot_operation_value=None, amount=2, filtration=True):
    """ Likes last user_id's medias """

    self.logger.info("Liking user_%s's feed:" % userObject['full_name'])
    medias = self.get_user_medias(userObject['instagram_user_id'], filtration=filtration)
    if not medias:
        self.logger.info(
            "None medias received: account is closed or medias have been filtered.")
        return False
    return self.like_medias(medias[:amount], bot_operation=bot_operation, bot_operation_value=bot_operation_value)


def like_own_followers(self, likesAmount=100):
    nrLikesPerFollower = 2
    followersAmount = likesAmount / nrLikesPerFollower

    batchSize = followersAmount
    followers = []
    securityBreak = 0
    followersResult = 0

    self.logger.info(
        "Going to retrieve from database %s followers to perform %s likes " % (followersAmount, likesAmount))
    totalFollowersResult = api_db.fetchOne(
        "select count(*) as total_followers from followers where id_user=%s order by id_follower asc",
        self.web_application_id_user)

    self.logger.info('Total followers: %s', totalFollowersResult['total_followers'])
    sqlLimitFromWhere = randint(0, (totalFollowersResult['total_followers'] - batchSize))

    self.logger.info('Start getting followers starting with index: %s', sqlLimitFromWhere)
    while len(followers) <= followersAmount and securityBreak < 100 and followersResult != None:

        followersResult = api_db.select("select * from followers where id_user=%s order by id_user asc limit %s,%s",
                                        self.web_application_id_user, sqlLimitFromWhere, batchSize)

        # nothing left in db
        if len(followersResult) < 1:
            self.logger.info("Nothing left in database, going to continue !")
            followersResult = None
            break

        filteredFollowers = []
        for f in followersResult:

            # check if this follower is valid
            f['instagram_user_id'] = f['instagram_id_follower']

            if self.check_user(f) == True:
                filteredFollowers.append(f)

            sleep_time = randint(1, 3)
            self.logger.info("Sleeping %s seconds" % sleep_time)
            time.sleep(sleep_time)

        followers = followers + filteredFollowers

        self.logger.info(
            "Iteration %s ,received %s followers, after filtration remained %s followers. Total received %s followers" % (
                securityBreak, len(followersResult), len(filteredFollowers), len(followers)))

        securityBreak = securityBreak + 1
        sqlLimitFromWhere += sqlLimitFromWhere + batchSize

    followers = followers[:followersAmount]

    self.logger.info("Total received %s followers from database. Going to start liking !" % len(followers))

    totalLiked = 0

    for f in followers:
        if not limits.check_if_bot_can_like(self):
            self.logger.info("Out of likes for today.")
            return
        totalLiked = totalLiked + self.like_user(userObject=f, bot_operation="like_own_followers",
                                                 amount=nrLikesPerFollower)

    self.logger.info('Total liked %s posts of your own followers !', totalLiked)

    return totalLiked


# this function is used to decide if the follower worth liking
def check_if_own_follower_is_valid(self, follower):
    self.logger.info('Going to check user: %s if worth liking/following ' % follower['full_name'])

    exit()
    return True


def like_users(self, user_ids, nlikes=None, filtration=True):
    for user_id in user_ids:
        if not limits.check_if_bot_can_like(self):
            self.logger.info("Out of likes for today.")
            return
        self.like_user(user_id, amount=nlikes, filtration=filtration)


def like_hashtag(self, hashtag, amount=None):
    self.logger.info("Going to like %s media with hashtag #%s." % (amount, hashtag))
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


    self.logger.info('Going to like %s followers of user: %s' % (amount, userObject['username']))

    result = self.get_user_followers(user_object=userObject, amount=amount, next_max_id=userObject['next_max_id'])

    with open('data.txt', 'w') as outfile:
        json.dump(result, outfile)

    exit()

    if len(result['followers']) == 0:
        self.logger.info("No followers received for user: %s ! SKIPPING" % userObject['user'])
        exit(0)

    followers = []
    iteration = 0
    securityBreak = 0

    self.logger.info("Going to check users")

    while len(followers) <= amount and securityBreak < 300:

        iteration = iteration + 1
        securityBreak = securityBreak + 1

        follower = result['followers'][iteration]

        # check if this follower is valid -> this might not be required / usefull
        follower['instagram_user_id'] = follower['pk']

        if self.check_user(follower) == True:
            followers.append(follower)

        sleep_time = randint(1, 3)
        self.logger.info("Sleeping %s seconds" % sleep_time)
        time.sleep(sleep_time)
        self.logger.info("Current followers %s:", len(followers))

    self.logger.info("Total received %s followers" % len(followers))
    followers = followers[:amount]

    totalLiked = 0
    nrLikesPerFollower = 1



    for f in followers:
        if not limits.check_if_bot_can_like(self):
            self.logger.info("Out of likes for today.")
            return totalLiked
        totalLiked = totalLiked + self.like_user(userObject=f, bot_operation="like_own_followers",bot_operation_value=userObject['user'],amount=nrLikesPerFollower)

    self.logger.info('Total liked %s posts of your own followers !', totalLiked)

    return totalLiked
