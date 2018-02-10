import time
import psutil
import logging
import os
import signal

logging.basicConfig(format='%(asctime)s %(message)s',filename='/home/instabot-log/stop_bot.log',level=logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger = logging.getLogger('[l4l]')
logger.setLevel(logging.DEBUG)
logger.addHandler(ch)

def killProcess(pid):
	logger.info("killProcess: killing process: %s",pid)
	os.kill(pid, signal.SIGTERM) 

def stopProcesses():
	logger.info("stopProcesses:Searching process...")
	
	for p in psutil.process_iter():
		cmdline=p.cmdline()
		processname = 'angie_idc'
		if len(cmdline)>0:
			if processname in cmdline[0]:
				logger.info("stopProcesses:Found %s, pid %s, going to kill it" % (cmdline[0], p.pid))
				killProcess(p.pid)
				
	logger.info("stopProcesses: DONE")

stopProcesses()
	