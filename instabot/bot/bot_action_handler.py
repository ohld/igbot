"""
    All methods must return media_ids that can be
    passed into e.g. like() or comment() functions.
"""

from ..api import api_db
import datetime
import json
from random import randint
import calendar


def getInitialActionAmount(self, id_campaign):
    result={}
    result['calculatedAmount']={}
    result['initialAmount']={}
    result['accountMaturity']={}
    result['accountMaturity']['reachedMaturity']=False
    
    maximumLikeAmountResult = api_db.fetchOne("select * from bot_config where `key`='maximum_like_amount'")
    result['initialAmount']['maximumLikeAmount']=int(maximumLikeAmountResult['value'])

    maximumFollowAmountResult = api_db.fetchOne("select * from bot_config where `key`='maximum_follow_amount'")
    result['initialAmount']['maximumFollowAmount'] = int(maximumFollowAmountResult['value'])

    minimumLikeAmountResult = api_db.fetchOne("select * from bot_config where `key`='minimum_like_amount'")
    result['initialAmount']['minimumLikeAmount'] = int(minimumLikeAmountResult['value'])

    minimumFollowAmountResult = api_db.fetchOne("select * from bot_config where `key`='minimum_follow_amount'")
    result['initialAmount']['minimumFollowAmount'] = int(minimumFollowAmountResult['value'])

    result['initialAmount']['minimumActionAmount'] = result['initialAmount']['minimumLikeAmount'] +result['initialAmount']['minimumFollowAmount']
    result['initialAmount']['maximumActionAmount'] = result['initialAmount']['maximumLikeAmount'] + result['initialAmount']['maximumFollowAmount']

    
    self.logger.info("getInitialActionAmount: Default bot configuration is:", result)
    
    #check maturity of account
    accountIsFullyFunctionalAfter=90
    campaign = api_db.fetchOne("select campaign.timestamp, percentage_amount, month_start,month_end from campaign join instagram_account_type using (id_account_type) where id_campaign=%s", id_campaign)
   
    d0 = campaign['timestamp']
    d1 = datetime.datetime.now()
    delta = d1 - d0
    
    if delta.days>=accountIsFullyFunctionalAfter:
        result['calculatedAmount']=result['initialAmount']
        result['accountMaturity']['reachedMaturity']=True
        self.logger.info("getInitialActionAmount: Account is fullyFunctional ! %s days passed since signup. Minimum is %s" % (delta.days, accountIsFullyFunctionalAfter))
        return result
    
    #check maturity if the account
    self.logger.info("getInitialActionAmount: Going to calculated action number based on account type: month_start: %s, month_end:%s, percentage: %s" % (campaign['month_start'],campaign['month_end'], campaign['percentage_amount']))

    result['accountMaturity']['usage_percentage'] = campaign['percentage_amount']
    result['calculatedAmount']['maximumLikeAmount']= int(round(result['initialAmount']['maximumLikeAmount'] * campaign['percentage_amount'] / 100))
    result['calculatedAmount']['maximumFollowAmount']= int(round(result['initialAmount']['maximumFollowAmount'] * campaign['percentage_amount'] / 100))
    result['calculatedAmount']['minimumLikeAmount']= int(round(result['initialAmount']['minimumLikeAmount'] * campaign['percentage_amount'] / 100))
    result['calculatedAmount']['minimumFollowAmount']= int(round(result['initialAmount']['minimumFollowAmount'] * campaign['percentage_amount'] / 100))

    result['calculatedAmount']['minimumActionAmount'] = result['calculatedAmount']['minimumLikeAmount'] +result['calculatedAmount']['minimumFollowAmount']
    result['calculatedAmount']['maximumActionAmount'] = result['calculatedAmount']['maximumLikeAmount'] + result['calculatedAmount']['maximumFollowAmount']
    
    self.logger.info("getInitialActionAmount: After applying %s percentage, the result is: %s" % (campaign['percentage_amount'], result))
    return result
    

#this function is used to retrieve the configuration if it is stoped and restarted
def resumeOperation(self, id_campaign):
  self.logger.info("resumeOperation: trying to resume")
  resumeResult = api_db.fetchOne("SELECT * FROM campaign_log WHERE DATE(`timestamp`) = CURDATE() and id_campaign=%s",id_campaign)
  
  if resumeResult is None:
    self.logger.info("resumeOperation: Could not resume, going to start from scratch !")
    return None

  self.logger.info("resumeOperation: Checkpoint was found, id: %s ",resumeResult['id_log'])
  result = {}
  self.id_log = resumeResult['id_log']
  result['like_amount']=resumeResult['expected_like_amount']
  result['follow_amount']=resumeResult['expected_follow_amount']
  
  return result

  
def getAmountDistribution(self, id_campaign):
  
    resume = resumeOperation(self,id_campaign)
    
    if resume is not None and resume['like_amount'] is not None and resume['follow_amount'] is not None:
      self.logger.info("getAmountDistribution: going to resume this amount: %s",resume)
      return resume
    
    categories = api_db.select("select * from action_amount_distribution")

    foundRightCategory = False
    securityBreak=10
    iteration = 0

    now = datetime.datetime.now()
    currentMonthNumberOfDays =  calendar.monthrange(now.year, now.month)[1]

    initialActionAmountResult = getInitialActionAmount(self, id_campaign)

    #maybe this while can be extracted separately
    while foundRightCategory==False and iteration<securityBreak and len(categories)>0:
        selectedCategoryIndex = randint(0, len(categories) - 1)

        #check if selected category is still available
        daysForThisCategory = int(round(currentMonthNumberOfDays * categories[selectedCategoryIndex]['percentage_amount']/100))

        

        amountToPerform = None
        if categories[selectedCategoryIndex]['type'] == "minimum":
          amountToPerform = "<="+str(initialActionAmountResult['calculatedAmount']['minimumActionAmount'])
          
        elif categories[selectedCategoryIndex]['type'] == "maximum":
          amountToPerform = ">="+str(initialActionAmountResult['calculatedAmount']['maximumActionAmount'])
          
        elif categories[selectedCategoryIndex]['type'] == "between":
          amountToPerform = "between "+str(initialActionAmountResult['calculatedAmount']['minimumActionAmount']) + " and "+str(initialActionAmountResult['calculatedAmount']['maximumActionAmount'])
          
        query = " select count(*) as total from  (select count(*) as total, date(timestamp) from bot_action " \
                " WHERE MONTH(timestamp) = MONTH(CURRENT_DATE()) " \
                " AND YEAR(timestamp) = YEAR(CURRENT_DATE()) and id_campaign=%s " \
                " group by date(timestamp) having count(*) "+amountToPerform + " " \
                " order by date(timestamp) desc) my_table"

        result = api_db.fetchOne(query, id_campaign)
        #self.logger.info("getAmountDistribution: %s",query)
        self.logger.info("getAmountDistribution: Selected category: %s, iteration %s, daysForThisCategory: %s, usedDays: %s" % (
        categories[selectedCategoryIndex], iteration, daysForThisCategory, result['total']))

        usedDaysForThisCategory = result['total']
        if result['total']<daysForThisCategory:
          foundRightCategory = categories[selectedCategoryIndex]
          break
        
        iteration = iteration + 1
        del categories[selectedCategoryIndex]
       
    self.logger.info("getAmountDistribution: Choosed category: %s ",foundRightCategory)
    
    result={}
    
    if foundRightCategory['type'] == "minimum":
      result['like_amount'] = initialActionAmountResult['calculatedAmount']['minimumLikeAmount']
      result['follow_amount'] = initialActionAmountResult['calculatedAmount']['minimumFollowAmount']
          
    elif foundRightCategory['type'] == "maximum":
      result['like_amount'] = initialActionAmountResult['calculatedAmount']['maximumLikeAmount']
      result['follow_amount'] = initialActionAmountResult['calculatedAmount']['maximumFollowAmount']
          
    else:
      #between
      result['like_amount'] = randint(initialActionAmountResult['calculatedAmount']['minimumLikeAmount']+1, initialActionAmountResult['calculatedAmount']['maximumLikeAmount']-1)
      result['follow_amount'] = randint(initialActionAmountResult['calculatedAmount']['minimumFollowAmount']+1, initialActionAmountResult['calculatedAmount']['maximumFollowAmount']-1)
    
    #create the log in database
    log={}
    log['amount_selected_category'] = {}
    log['amount_selected_category']['category']=foundRightCategory
    log['amount_selected_category']['daysAllocatedForThisCategory'] = daysForThisCategory
    log['amount_selected_category']['usedDaysForThisCategory'] = usedDaysForThisCategory
    log['amount_selected_category']['currentMonthNumberOfDays'] = currentMonthNumberOfDays
    log['expected_amount']=result
    log['initial_action_amount']=initialActionAmountResult


    logJson = json.dumps(log)

    id = api_db.insert("insert into campaign_log (`id_campaign`,`details`, `name`, `expected_like_amount`, `expected_follow_amount`, `id_amount_distribution`, `timestamp`) values (%s,%s,%s,%s,%s,%s,now())",id_campaign,logJson,'LOG_CAMPAIGN_START',result['like_amount'],result['follow_amount'],foundRightCategory['id_amount_distribution'])
    self.id_log=id
    self.logger.info("getAmountDistribution: Final action amount: %s",result)
    self.logger.info("getAmountDistribution: ID_LOG: %s",id)

    return result


def getLikeAmount(self,id_campaign, calculatedAmount):
  likesAmount=calculatedAmount['like_amount']

  hasLikesOperation= api_db.fetchOne("select count(*) as rows from campaign_config where id_campaign=%s and configName like %s and enabled=1",id_campaign, "like_"+"%")
  if hasLikesOperation['rows']==0:
    #todo exclude bot account
    usersLikeForLike = api_db.fetchOne('select count(*) as total_users  from users join user_subscription on (users.id_user = user_subscription.id_user)  join campaign on (users.id_user = campaign.id_user) join user_rol on (users.id_user=user_rol.id_user) where (user_subscription.end_date>now() or user_subscription.end_date is null)   and campaign.id_campaign!=%s and user_rol.rol_id=1 order by users.id_user',id_campaign)
    self.logger.info("getLikeAmount: Total number of likeForLike users: %s", usersLikeForLike['total_users'])
    self.logger.info("getLikeAmount: Campaign id: %s did not set any like operations ! Going to perform only %s likeForLike:!" % (id_campaign, usersLikeForLike['total_users']))
    return usersLikeForLike['total_users']
  
  self.logger.info("getLikeAmount: Campaign id %s wants to perform %s amount of likes" % (id_campaign,likesAmount))
      
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
    
  return followAmount

def getLikesPerformed(self, dateParam):
  likesPerformed=api_db.fetchOne('SELECT count(*) as no_op FROM bot_action where bot_operation like %s and date(timestamp)=%s and id_user=%s', "like"+"%", str(dateParam), self.web_application_id_user)
  
  if likesPerformed['no_op'] >0:
    self.logger.info("getLikesPerformed: Campaign id %s has  ALREADY performed %s likes. in day %s" % (self.id_campaign, likesPerformed['no_op'], dateParam))
  else:
    self.logger.info("getLikesPerformed: 0 likes PREVIOUSLY performed for campaign id  %s, in day %s" % (self.id_campaign,dateParam))
  
  return likesPerformed['no_op']


def getFollowPerformed(self,dateParam):
    
  #follows peformed during this day
  followsPerformed=api_db.fetchOne("SELECT count(*) as no_op FROM `bot_action` where (bot_operation like %s or bot_operation like %s) and date(timestamp)=%s and id_user=%s", "follow_"+"%","unfollow"+"%", str(dateParam), self.web_application_id_user)
  
  if followsPerformed['no_op'] >0:
    self.logger.info("getFollowAmount: Campaign id %s has ALREADY performed %s follow/unfollow, in day %s ." % (self.id_campaign, followsPerformed['no_op'],dateParam))  
  else:
    self.logger.info("getLikesPerformed: 0 follow ALREADY performed for campaign %s, in day %s" % (self.id_campaign,dateParam))
  
  return followsPerformed['no_op']