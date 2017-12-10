import MySQLdb
import sys
import json


def getConnection():
    db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                         user="angie_app",  # your username
                         passwd="angiePasswordDB",  # your password
                         db="angie_app")
    db.set_character_set('utf8mb4')
    dbc = db.cursor()
    dbc.execute('SET NAMES utf8mb4;')
    dbc.execute('SET CHARACTER SET utf8mb4;')
    dbc.execute('SET character_set_connection=utf8mb4;')

    return db


def getUserId(campaignId):
    if campaignId != False:
        row = fetchOne("select id_user from campaign where id_campaign=%s", campaignId)
        return row['id_user']
    else:
        return None


def getWebApplicationUser(id_user):
    if id_user != False:
        row = fetchOne("select * from users where id_user=%s", id_user)
        return row
    else:
        return False


def fetchOne(query, *args):
    db = getConnection()
    cur = db.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(query, args)
    db.close()
    return cur.fetchone()


def select(query, *args):
    db = getConnection()
    cur = db.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(query, args)
    rows = cur.fetchall()
    db.close()
    return list(rows)


def insert(query, *args):
    db = getConnection()
    cur = db.cursor()
    cur.execute(query, args)
    db.commit()
    id = cur.lastrowid
    db.close()
    return id

def updateCampaignChekpoint(key, value, id_campaign):
  query='INSERT INTO campaign_checkpoint (id_campaign, _key, value, timestamp) VALUES(%s, %s, %s, CURDATE()) ON DUPLICATE KEY UPDATE  value=%s'
  
  id = insert(query, id_campaign, key, value, value)
  
  return id
  
  
def insertBotAction(*args):
    query = "insert into bot_action (id_campaign, id_user, instagram_id_user, " \
            "full_name, username, user_image, post_id, post_image, " \
            "post_link,bot_operation,bot_operation_value,id_log,timestamp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())"

    id = insert(query, *args)
    return id


def insertOwnFollower(*args):
    query = "insert into own_followers (id_user,instagram_id_user,full_name,username,user_image,is_verified,timestamp) " \
            " VALUES (%s,%s,%s,%s,%s,%s,now()) ON DUPLICATE KEY UPDATE instagram_id_user=instagram_id_user"

    id = insert(query, *args)
    return id


def insertUserFollower(*args):
    query = "insert into instagram_user_followers (fk,instagram_id_user,full_name,username,user_image,is_verified,timestamp) " \
            " VALUES (%s,%s,%s,%s,%s,%s,now()) ON DUPLICATE KEY UPDATE instagram_id_user=instagram_id_user"

    id = insert(query, *args)
    return id


def getBotIp(bot, id_user, id_campaign):
    # get the ips ordered by how many time they are currently in use
    query = " select ip_bot.id_ip_bot,total,ip_bot.ip from ( " \
            " select id_ip_bot, 0 as total from ip_bot " \
            " where id_ip_bot not in  (select id_ip_bot from campaign where id_ip_bot is not null) " \
            " UNION " \
            " select campaign.id_ip_bot,count(*) as total from campaign" \
            " where id_ip_bot is not null" \
            " group by id_ip_bot " \
            " having count(*)<5 " \
            " order by total asc ) tbl" \
            " join ip_bot on (tbl.id_ip_bot=ip_bot.id_ip_bot) " \
            " order by total asc " \
            " limit 1;"

    result = fetchOne(query)

    if result is None:
        bot.logger.warning("getBotIp: Could not find an ip for user %s", id_user)
        exit()

    if result['total'] > 2:
        bot.logger.warning("getBotIp: Error: %s is used % times." % (result['ip'], result['total']))



    bot.logger.info("User %s, received ip: %s" % (id_user, result['ip']))
    insert('update campaign set id_ip_bot=%s where id_campaign=%s', result['id_ip_bot'], id_campaign)

    return result['ip']