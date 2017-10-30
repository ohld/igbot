import MySQLdb
import sys
import json



def getConnection():

    db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                         user="angie_app",  # your username
                         passwd="angiePasswordDB",  # your password
                         db="instaboost")
    db.set_character_set('utf8mb4')
    dbc = db.cursor()
    dbc.execute('SET NAMES utf8mb4;')
    dbc.execute('SET CHARACTER SET utf8mb4;')
    dbc.execute('SET character_set_connection=utf8mb4;')

    return db

def getUserId(campaignId):
    if campaignId!=False:
        row = fetchOne("select id_user from campaign where id_campaign=%s",campaignId)
        return row['id_user']
    else:
        return False


def getWebApplicationUser(id_user):
    if id_user!=False:
        row = fetchOne("select * from users where id_user=%s",id_user)
        return row
    else:
        return False

def fetchOne(query,*args):
    db = getConnection()
    cur = db.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(query,args)
    db.close()
    return cur.fetchone()

def select(query, *args):
    db=getConnection()
    cur = db.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(query,args)
    rows = cur.fetchall()
    db.close()
    return list(rows)

def insert(query, *args):
    db = getConnection()
    cur = db.cursor()
    cur.execute(query,args)
    db.commit()
    id=cur.lastrowid
    db.close()
    return id

def insertBotAction(*args):

    query="insert into bot_action (id_campaign, id_user, instagram_id_user, " \
          "full_name, username, user_image, post_id, post_image, " \
          "post_link,bot_operation,bot_operation_value,id_log) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    id = insert(query,*args)
    return id

def insertOwnFollower(*args):

    query="insert into own_followers (id_user,instagram_id_user,full_name,username,user_image,is_verified) " \
          " VALUES (%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE instagram_id_user=instagram_id_user"

    id = insert(query,*args)
    return id
  
def insertUserFollower(*args):
  query="insert into instagram_user_followers (fk,instagram_id_user,full_name,username,user_image,is_verified) " \
  " VALUES (%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE instagram_id_user=instagram_id_user"

  id = insert(query,*args)
  return id

def getBotIp(id_user):
 
  #get the ips ordered by how many time they are currently in use
  query="
  select id_ip_bot, 0 as total
  from ip_bot
  where id_ip_bot not in  (select id_ip_bot from campaign)
  UNION
  select campaign.id_ip_bot,count(*) as total from campaign 
  where id_ip_bot is not null
  group by id_ip_bot having count(*)<3
  order by total asc"
  
  result = fetchOne(query)
  
  
  
  
  