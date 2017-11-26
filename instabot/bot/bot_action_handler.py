"""
    All methods must return media_ids that can be
    passed into e.g. like() or comment() functions.
"""

from ..api import api_db
import datetime
from random import randint
import calendar


#todo apply rules regarding account maturity
def getInitialActionAmount(self, id_campaign):
    result={}
    
    maximumLikeAmountResult = api_db.fetchOne("select * from bot_config where `key`='maximum_like_amount'")
    result['maximumLikeAmount']=int(maximumLikeAmountResult['value'])

    maximumFollowAmountResult = api_db.fetchOne("select * from bot_config where `key`='maximum_follow_amount'")
    result['maximumFollowAmount'] = int(maximumFollowAmountResult['value'])

    minimumLikeAmountResult = api_db.fetchOne("select * from bot_config where `key`='minimum_like_amount'")
    result['minimumLikeAmount'] = int(minimumLikeAmountResult['value'])

    minimumFollowAmountResult = api_db.fetchOne("select * from bot_config where `key`='minimum_follow_amount'")
    result['minimumFollowAmount'] = int(minimumFollowAmountResult['value'])

    result['minimumActionAmount'] = result['minimumLikeAmount'] +result['minimumFollowAmount']
    result['maximumActionAmount'] = result['maximumLikeAmount'] + result['maximumFollowAmount']

    
    self.logger.info("getInitialActionAmount: %s", result)
    
    #check maturity of account
    accountIsFullyFunctionalAfter=90
    campaign = api_db.fetchOne("select campaign.timestamp, percentage_amount, month_start,month_end from campaign join instagram_account_type using (id_account_type) where id_campaign=%s", id_campaign)
   
    d0 = campaign['timestamp']
    d1 = datetime.datetime.now()
    delta = d1 - d0
    
    if delta.days>=accountIsFullyFunctionalAfter:
      self.logger.info("getInitialActionAmount: Account is fullyFunctional ! %s days passed since signup. Minimum is %s" % (delta.days, accountIsFullyFunctionalAfter))
      return result
    
    #check maturity if the account
    self.logger.info("getInitialActionAmount: Going to apply percentage on Account type: %s", campaign)
    
    
    result['maximumLikeAmount']= int(round(result['maximumLikeAmount'] * campaign['percentage_amount'] / 100))
    result['maximumFollowAmount']= int(round(result['maximumFollowAmount'] * campaign['percentage_amount'] / 100))
    result['minimumLikeAmount']= int(round(result['minimumLikeAmount'] * campaign['percentage_amount'] / 100))
    result['maximumActionAmount']= int(round(result['maximumActionAmount'] * campaign['percentage_amount'] / 100))
    
    result['minimumActionAmount'] = result['minimumLikeAmount'] +result['minimumFollowAmount']
    result['maximumActionAmount'] = result['maximumLikeAmount'] + result['maximumFollowAmount']
    
    self.logger.info("getInitialActionAmount: After applying %s percentage, the result is: %s" % (campaign['percentage_amount'], result))
    return result
    

#this function is used to retrieve the configuration if it is stoped and restarted
def resumeOperation(self, id_campaign):
  self.logger.info("resumeOperation: trying to resume")
  resumeResult = api_db.fetchOne("SELECT * FROM campaign_log WHERE DATE(`timestamp`) = CURDATE() and id_campaign=%s",id_campaign)
  
  if resumeResult is None:
    return None
  
  result = {}
  self.id_log = resumeResult['id_log']
  result['like_amount']=resumeResult['expected_like_amount']
  result['follow_amount']=resumeResult['expected_follow_amount']
  
  return result

  
def getAmountDistribution(self, id_campaign):
  
    resume = resumeOperation(self,id_campaign)
    
    if resume is not None:
      self.logger.info("getAmountDistribution: going to resume %s",resume)
      return resume
    
    categories = api_db.select("select * from action_amount_distribution")

    foundRightCategory = False
    securityBreak=10
    iteration = 0

    now = datetime.datetime.now()
    currentMonthNumberOfDays =  calendar.monthrange(now.year, now.month)[1]

    initialActionAmount = getInitialActionAmount(self, id_campaign)
     
    #maybe this while can be extracted separately
    while foundRightCategory==False and iteration<securityBreak and len(categories)>0:
        selectedCategoryIndex = randint(0, len(categories) - 1)

        #check if selected category is still available
        daysForThisCategory = int(round(currentMonthNumberOfDays * categories[selectedCategoryIndex]['percentage_amount']/100))

        

        amountToPerform = None
        if categories[selectedCategoryIndex]['type'] == "minimum":
          amountToPerform = "<="+str(initialActionAmount['minimumActionAmount'])
          
        elif categories[selectedCategoryIndex]['type'] == "maximum":
          amountToPerform = ">="+str(initialActionAmount['maximumActionAmount'])
          
        elif categories[selectedCategoryIndex]['type'] == "between":
          amountToPerform = "between "+str(initialActionAmount['minimumActionAmount']) + " and "+str(initialActionAmount['maximumActionAmount'])
          
        query = " select count(*) as total from  (select count(*) as total, date(timestamp) from bot_action " \
                " WHERE MONTH(timestamp) = MONTH(CURRENT_DATE()) " \
                " AND YEAR(timestamp) = YEAR(CURRENT_DATE()) and id_campaign=%s " \
                " group by date(timestamp) having count(*) "+amountToPerform + " " \
                " order by date(timestamp) desc) my_table"

        result = api_db.fetchOne(query, id_campaign)
        self.logger.info("getAmountDistribution: %s",query)
        self.logger.info("getAmountDistribution: Selected category: %s, iteration %s, daysForThisCategory: %s, usedDays: %s" % (
        categories[selectedCategoryIndex], iteration, daysForThisCategory, result['total']))
        
        if result['total']<daysForThisCategory:
          foundRightCategory = categories[selectedCategoryIndex]
          break
        
        iteration = iteration + 1
        del categories[selectedCategoryIndex]
       
    self.logger.info("getAmountDistribution: Choosed %s category",foundRightCategory)
    
    result={}
    
    if foundRightCategory['type'] == "minimum":
      result['like_amount'] = initialActionAmount['minimumLikeAmount']
      result['follow_amount'] = initialActionAmount['minimumFollowAmount']
          
    elif foundRightCategory['type'] == "maximum":
      result['like_amount'] = initialActionAmount['maximumLikeAmount']
      result['follow_amount'] = initialActionAmount['maximumFollowAmount']
          
    else:
      #between
      result['like_amount'] = randint(initialActionAmount['minimumLikeAmount']+1, initialActionAmount['maximumLikeAmount']-1)
      result['follow_amount'] = randint(initialActionAmount['minimumFollowAmount']+1, initialActionAmount['maximumFollowAmount']-1)
    
    #create the log in database
    
    id = api_db.insert("insert into campaign_log (`id_campaign`, `name`, `expected_like_amount`, `expected_follow_amount`, `id_amount_distribution`, `timestamp`) values (%s,%s,%s,%s,%s,now())",id_campaign,'LOG_CAMPAIGN_START',result['like_amount'],result['follow_amount'],foundRightCategory['id_amount_distribution'])
    self.id_log=id
    self.logger.info("getAmountDistribution: ID_LOG: %s",id)
    
    return result


def getLikeAmount(self,id_campaign, calculatedAmount):
  likesAmount=calculatedAmount['like_amount']

  hasLikesOperation= api_db.fetchOne("select count(*) as rows from campaign_config where id_campaign=%s and configName like %s and enabled=1",id_campaign, "like_"+"%")
  if hasLikesOperation['rows']==0:
    self.logger.info("getLikeAmount: Campaign id: %s did not set any like operations ! Going to perform 0 likes !", id_campaign)
    return 0
  
  
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
def getFollowAmount(self,id_campaign, calculatedAmount):
  followAmount=calculatedAmount['follow_amount']
  
  hasFollowOperation = api_db.fetchOne(
        "select count(*) as rows from campaign_config where id_campaign=%s and (configName like %s or configName=%s) and enabled=1", id_campaign,
        "follow_" + "%","unfollow")
  
  if hasFollowOperation['rows']==0:
    self.logger.info("getFollowAmount: Campaign id: %s did not set any follow/unfollow operations ! Going to perform 0 follow/unfollow !", id_campaign)
    return 0
  
  
  self.logger.info("getFollowAmount: Campaign id %s wants to perform %s amount of follow/unfollow" % (id_campaign,followAmount))
  
  currentDate=str(datetime.date.today())
  
  #follows peformed during this day
  followsPerformed=api_db.fetchOne("SELECT count(*) as no_op FROM `bot_action` where (bot_operation like %s or bot_operation like %s) and date(timestamp)=%s and id_user=%s", "follow_"+"%","unfollow"+"%", currentDate, self.web_application_id_user)
  
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