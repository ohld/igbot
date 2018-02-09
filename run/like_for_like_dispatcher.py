import time
import psutil
import logging
import os
from instabot.api import api_db

logging.basicConfig(format='%(asctime)s %(message)s',filename='/home/instabot-log/like_for_like_dispatcher.log',level=logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger = logging.getLogger('[l4l]')
logger.setLevel(logging.DEBUG)
logger.addHandler(ch)

def pauseProcess(pid):
	logger.info("pauseProcess: pausing process: %s",pid)
	p = psutil.Process(pid)
	p.suspend()
	
def startLikeForLikeProcess(id_campaign):
	logger.info("startLikeForLikeProcess: Starting like for like process for campaign %s",id_campaign)
	
	logger.info("startLikeForLikeProcess: DONE !")

def getProcessPid(id_campaign):
	logger.info("getProcessPid:Searching process with id_campaign:%s ",id_campaign)
	for p in psutil.process_iter():
		cmdline=p.cmdline()
		processname = 'angie_idc'+str(id_campaign)
		if len(cmdline)>0:
			if processname in cmdline[0]:
				logger.info("getProcessPid:Found %s, pid %s" % (cmdline[0], p.pid))
				return p.pid
			
	logger.info("getProcessPid: Did not find any process for campaign %s",id_campaign)
	return False

def startLikeForLike(user):
	pid=getProcessPid(user['id_campaign'])
	if pid==False:
		logger.info("startLikeForLike: Bot process is not running for campaign %s. Going to start a new one",user['id_campaign'])
		#start process
		startLikeForLikeProcess(user['id_campaign'])
	else:
		#pause current process and start a new one
		logger.info("startLikeForLike: Bot process is sunning for campaign %s, going to pause it ",user['id_campaign'])
		pauseProcess(pid)
		startLikeForLikeProcess(user['id_campaign'])
	



#select users that have pending work to do
result = api_db.select("select users.id_user,email,username,campaign.password,campaign.id_campaign from users  join campaign on (users.id_user=campaign.id_user) join user_subscription on (users.id_user = user_subscription.id_user)  where (user_subscription.end_date>now() or user_subscription.end_date is null) and (select count(*) from user_post_log where id_user=users.id_user)<(select count(*) from user_post) and users.id_user=1");
#logger.info(result)
logger.info("Found %s users with pending work",len(result))
for user in result:
	logger.info("Going to process user %s",user['email'])
	#check if bot is already running for this campaign
	
	startLikeForLike(user)
	
	logger.info("Going to wait 1 seconds before processing another user !")
	time.sleep(1)
	
	
	

	