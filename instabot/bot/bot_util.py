"""
    All methods must return media_ids that can be
    passed into e.g. like() or comment() functions.
"""

from ..api import api_db
import math
import datetime
  
def getLikeAmount(self,id_campaign):
  likesAmount=0
  
  hasLikesOperation= api_db.fetchOne("select count(*) as rows from campaign_config where id_campaign=%s and configName like %s and enabled=1",id_campaign, "like_"+"%")
  if hasLikesOperation['rows']==0:
    self.logger.info("getLikeAmount: Campaign id: %s did not set any like operations ! Going to perform 0 likes !", id_campaign)
    return 0
  
  #get initial amount to perform
  campaign = api_db.fetchOne("select amount_likes_day,amount_follow_day from campaign where id_campaign=%s", id_campaign)
  likesAmount=campaign['amount_likes_day']
  
  self.logger.info("getLikeAmount: Campaign id %s wants to perform %s amount of likes" % (id_campaign,likesAmount))
  
  currentDate=str(datetime.date.today())
  likesPerformed=api_db.fetchOne('SELECT count(*) as no_op FROM bot_action where bot_operation like %s and date(timestamp)=%s and id_user=%s', "like"+"%", currentDate, self.web_application_id_user)
  
  if likesPerformed['no_op'] >0:
    self.logger.info("getLikeAmount: Campaign id %s has  already performed %s likes. Going to perform %s amount of likes" % (id_campaign, likesPerformed['no_op'], likesAmount-likesPerformed['no_op']))
  
  likesAmount = likesAmount - likesPerformed['no_op']
  
  #safe check
  if likesAmount < 0:
    likesAmount=0
    
  
  return likesAmount
  
# there is one strange thing about the follow amount:
# if the user has selected only the unfollow operation, the total follow/unfollow amount should be devided by 2
def getFollowAmount(self,id_campaign):
  followAmount=0
  
  hasFollowOperation = api_db.fetchOne(
        "select count(*) as rows from campaign_config where id_campaign=%s and (configName like %s or configName=%s) and enabled=1", id_campaign,
        "follow_" + "%","unfollow")
  
  if hasFollowOperation['rows']==0:
    self.logger.info("getFollowAmount: Campaign id: %s did not set any follow/unfollow operations ! Going to perform 0 follow/unfollow !", id_campaign)
    return 0
  
  #get initial amount to perform
  campaign = api_db.fetchOne("select amount_likes_day,amount_follow_day from campaign where id_campaign=%s", id_campaign)
  followAmount=campaign['amount_follow_day']
  
  self.logger.info("getFollowAmount: Campaign id %s has set %s amount of follows" % (id_campaign,followAmount))
  
  currentDate=str(datetime.date.today())
  
  #follows peformed during this day
  followsPerformed=api_db.fetchOne("SELECT count(*) as no_op FROM `bot_action` where (bot_operation like %s or bot_operation like %s) and date(timestamp)=%s and id_user=%s", "follow_"+"%s","unfollow"+"%", currentDate, self.web_application_id_user)
  
  if followsPerformed['no_op'] >0:
    self.logger.info("getFollowAmount: Campaign id %s has already performed %s follows operations. Going to perform %s amount of follows" % (id_campaign, followsPerformed['no_op'], followAmount-followsPerformed['no_op']))  
  
  followAmount = followAmount - followsPerformed['no_op']
  
  #safe check
  if followAmount < 0:
    followAmount=0
    
  #check if the user has selected only unfollow operation
  if hasFollowOperation['rows']==1 and followAmount>0:
    hasOnlyUnfollowSelected = api_db.fetchOne("select count(*) as rows from campaign_config where id_campaign=%s and configName=%s and enabled=1", id_campaign,"unfollow")
    if hasOnlyUnfollowSelected['rows']==1:
      self.logger.info("getFollowAmount: User has selected only unfollow operation. Initial amount of %s will be divided by 2: %s " % (followAmount, followAmount/2))
      followAmount=followAmount/2
  
  
    

  return followAmount
  
def getBotOperations(self, id_campaign):

    totalLikePercentage = 0
    totalFollowPercentage = 0
    totalLikeOperations=0
    totalFollowOperations=0

    operations = api_db.select("SELECT configName,id_config, percentageAmount FROM campaign_config where id_campaign=%s and enabled=1",
                               id_campaign)
    for operation in operations:

        if 'like_other_users_followers' in operation['configName'] or 'follow_other_users_followers' in operation['configName']:
            users = api_db.select("select * from instagram_users where id_config=%s and enabled=1",
                                  operation['id_config'])
            operation['list'] = users

        if 'like_posts_by_hashtag' in operation['configName'] or 'follow_users_by_hashtag' in operation['configName']:
            hashtags = api_db.select("select * from instagram_hashtags where id_config=%s and enabled=1",
                                     operation['id_config'])
            operation['list'] = hashtags

        if 'like_posts_by_location' in operation['configName'] or 'follow_users_by_location' in operation['configName']:
            locations = api_db.select("select * from instagram_locations where id_config=%s and enabled=1",
                                      operation['id_config'])
            operation['list'] = locations

        if 'like' in operation['configName']:
            totalLikePercentage += operation['percentageAmount']
            totalLikeOperations+=1

        elif 'follow' in operation['configName']:
            totalFollowPercentage += operation['percentageAmount']

            #the unfollow operation has a fixed percentage of 40%
            if operation['configName']!="unfollow":
                totalFollowOperations+=1


        parameters = api_db.select("select * from campaign_config_parameters where id_config=%s",
                                   operation['id_config'])

        operation['parameters'] = parameters


    #apply percentage
    if totalLikePercentage<100 and totalLikePercentage>0:
        self.logger.info("BOTUTIL: Unused percentage is %s, going to distribute it to %s operations" % (100-totalLikePercentage, totalLikeOperations))
        remainingLikePercentage = math.ceil (math.ceil(100-totalLikePercentage) / math.ceil(totalLikeOperations))
        self.logger.info("BOTUTIL: Each operation will receive %s extra percentage !", remainingLikePercentage)

        for operation in operations:
            if 'like' in operation['configName']:
                operation['percentageAmount']+=remainingLikePercentage

    if totalFollowPercentage<100 and totalFollowPercentage>0:
        
        self.logger.info("BOTUTIL: Unused percentage is %s, going to distribute it to %s operations" % (100- totalFollowPercentage, totalFollowOperations))
        
        if totalFollowOperations==0:
          self.logger.info("BOTUTIL: no available operations of type follow. Probably it is set the unfollow operation with fixed percentage !")
        else:
          remainingFollowPercentage = math.ceil(math.ceil(100 - totalFollowPercentage) / math.ceil(totalFollowOperations))
          self.logger.info("BOTUTIL: Each operation of type follow will receive %s extra percentage !", remainingFollowPercentage)

          for operation in operations:
              if 'follow' in operation['configName'] and operation['configName']!="unfollow":
                  operation['percentageAmount'] += remainingFollowPercentage

    for op in operations:
        self.logger.info("Percentage: %s , Amount: %s" % (op['percentageAmount'], op['configName']))


    return operations