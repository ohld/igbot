from tqdm import tqdm

from . import limits
from . import delay
from ..api import api_db
import json


def unfollowBotCreatedFollowings(self, amount):
    # check if user wants to unfollow
    userWantsToUnfollow = getIfUserWantsToUnfollow(self)
    if userWantsToUnfollow == False:
        self.logger.info("unfollowBotCreatedFollowings: User does not want to unfollow !")
        return False
    else:
        self.logger.info("unfollowBotCreatedFollowings: User wants to unfollow after %s hours" % userWantsToUnfollow['value'])

    self.logger.info("unfollowBotCreatedFollowings: Going to unfollow %s users from bot created followings", amount)
    selectFollowings = "select * from bot_action where  bot_operation like %s and timestamp< (NOW() - INTERVAL %s HOUR) and id_user= %s and bot_operation_reverted is null order by timestamp asc limit %s"

    followings = api_db.select(selectFollowings, 'follow' + '%', userWantsToUnfollow['value'],
                               self.web_application_id_user,
                               amount)
    self.logger.info("unfollowBotCreatedFollowings: Found %s users in database to unfollow", len(followings))

    totalUnfollow = 0
    for f in followings:
        status = unfollow(self, f['instagram_id_user'])
        if status == True:

            lastBotAction = api_db.insertBotAction(self.id_campaign, self.web_application_id_user,
                                                   f['instagram_id_user'], f['full_name'], f['username'],
                                                   f['user_image'], f['post_id'], f['post_image'],
                                                   f['post_link'], 'unfollow_bot_created_followings', None, self.id_log)

            api_db.insert("update bot_action set bot_operation_reverted=%s where id=%s", lastBotAction, f['id'])
            totalUnfollow = totalUnfollow + 1
        else:
            self.logger.info("unfollowBotCreatedFollowings: Error: could not follow %s. Going to disable this follower! ", f['instagram_id_user'])
            api_db.insert("update bot_action set bot_operation_reverted=%s where id=%s", None, f['id'])
        if totalUnfollow > amount:
            break

        self.logger.info("unfollowBotCreatedFollowings: Total users unfollowed: %s", totalUnfollow)

    return totalUnfollow


def getIfUserWantsToUnfollow(self):
    query = 'select _key,value from  campaign_config join campaign_config_parameters using (id_config) where configName="unfollow"  and id_campaign= %s and _key="after_x_hours" and campaign_config.enabled=1'

    result = api_db.fetchOne(query, self.id_campaign)
    if not result:
        return False

   
    return result


def unfollow(self, user_id):
    self.logger.info('unfollow: Going to UN-Follow user_id: %s', user_id)

    delay.unfollow_delay(self)
    if super(self.__class__, self).unfollow(user_id):
        self.logger.info('Unfollowed user_id: %s', user_id)
        self.total_unfollowed += 1
        return True


def unfollow_users(self, user_ids):
    broken_items = []
    self.logger.info("unfollow_users: Going to unfollow %d users." % len(user_ids))
    user_ids = set(map(str, user_ids))
    filtered_user_ids = list(set(user_ids) - set(self.whitelist))
    if len(filtered_user_ids) != len(user_ids):
        self.logger.info(
            "unfollow_users: After filtration by whitelist %d users left." % len(filtered_user_ids))
    for user_id in tqdm(filtered_user_ids):
        if not self.unfollow(user_id):
            delay.error_delay(self)
            broken_items = filtered_user_ids[filtered_user_ids.index(user_id):]
            break
    self.logger.info("unfollow_users: DONE: Total unfollowed %d users. " %
                     self.total_unfollowed)
    return broken_items


def unfollow_non_followers(self, n_to_unfollows=None):
    self.logger.info("Unfollowing non-followers")
    self.update_unfollow_file()
    print("\n\033[91m ===> Start Unfollowing Non_Followers List <===\033[0m")
    unfollow_file = "unfollow.txt"
    new_unfollow_list = list(line.strip() for line in open(unfollow_file))
    for user in tqdm(new_unfollow_list[:n_to_unfollows]):  # select only first n_to_unfollows users to unfollow
        self.unfollow(user)
    print(
        "\n\033[91m ===> Unfollow Non_followers , Task Done <===\033[0m")


def unfollow_everyone(self):
    self.following = self.get_user_following(self.user_id)
    self.unfollow_users(self.following)


def update_unfollow_file(self):  # Update unfollow.txt
    self.logger.info("Updating unfollow.txt ...")
    print("\n\033[92m Calculating Non Followers List  \033[0m")
    followings = self.get_user_following(self.user_id)  # getting following
    followers = self.get_user_followers(self.user_id)  # getting followers
    friends_file = self.read_list_from_file(
        "friends.txt")  # same whitelist (just user ids)
    nonfollowerslist = list(
        (set(followings) - set(followers)) - set(friends_file))
    followed_file = "followed.txt"
    followed_list = self.read_list_from_file(followed_file)
    unfollow_list = []
    unfollow_list += [x for x in followed_list if x in nonfollowerslist]
    unfollow_list += [x for x in nonfollowerslist if x not in followed_list]
    unfollow_file = self.read_list_from_file("unfollow.txt")
    new_unfollow_list = []
    new_unfollow_list += [x for x in unfollow_file if x in unfollow_list]
    new_unfollow_list += [x for x in unfollow_list if x not in unfollow_file]
    print("\n Writing to unfollow.txt")
    out = open('unfollow.txt', 'w')
    for line in new_unfollow_list:
        out.write(str(line) + "\n")
    print("\n Updating unfollow.txt , Task Done")
