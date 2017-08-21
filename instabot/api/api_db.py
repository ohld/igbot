import MySQLdb
import sys
import json



def getConnection():

    db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                         user="root",  # your username
                         passwd="password",  # your password
                         db="instaboost")
    return db

def getUserId(campaignId):
    row = fetchOne("select id_user from campaign where id_campaign=%s",campaignId)
    return row['id_user']


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
    return True




