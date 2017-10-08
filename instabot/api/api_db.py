import MySQLdb
import sys
import json



def getConnection():

    db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                         user="root",  # your username
                         passwd="password",  # your password
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
    return rows

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

def insertFollower(*args):

    query="insert into followers (id_user,instagram_id_follower,full_name,username,user_image,is_verified) " \
          " VALUES (%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE instagram_id_follower=instagram_id_follower"

    id = insert(query,*args)
    return id
    



