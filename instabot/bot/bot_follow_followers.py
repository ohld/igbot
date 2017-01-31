import time
import random
import json
from tqdm import tqdm

def follow_followers(bot,user_id):

    if not user_id:
        return False

    print("Follow followers of: %i" % user_id)

    followers = bot.getTotalFollowers(user_id)
    follower_ids = []

    for f in followers:
    	follower_ids.append(f['pk'])

    for i in tqdm(follower_ids, desc="Following followers"):
    	# print ("Following %i's feed:" % i)
    	bot.follow(i)
    	time.sleep(10 + 20 * random.random())
