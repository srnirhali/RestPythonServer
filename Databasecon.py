# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 12:56:52 2019

@author: Dell
"""

import json
import mysql.connector
import datetime

mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="cat@123",
      database="newsdatabase"
    )

def default_date(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
    
def getAllNewsDB():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id,source_url,source_name,claim,claim_urls,label,publish_date,author FROM news")
    row_headers=[x[0] for x in mycursor.description]
    myresult = mycursor.fetchall()
    json_data=[]
    for result in myresult:
        json_data.append(dict(zip(row_headers,result)))
    return json_data

def isUserAvailable(userName):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM users where user_name='{}'".format(userName))
    
    print(mycursor.fetchall())
    if mycursor.rowcount==0:
        return False
    return True

def isNewsAvailable(number):
    number = int(number)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id FROM news where id={}".format(number))
    mycursor.fetchall()
    if mycursor.rowcount==0:
        return False
    return True
    
def createUser(userName):
    mycursor = mydb.cursor()
    mycursor.execute("insert into users(user_name,last_id) values('{}',1) ".format(userName))
    mydb.commit()
    return mycursor.rowcount

def getUserDetails(userName):
    if isUserAvailable(userName):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM users where user_name='{}'".format(userName))
        myresult = mycursor.fetchall()
        row_headers=[x[0] for x in mycursor.description]
        json_data=[]
        for result in myresult:
            json_data.append(dict(zip(row_headers,result)))
            return json_data
    else:
        return None

def getNewsByID(number):
    number = int(number)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id,source_url,source_name,claim,claim_urls,label,publish_date,author FROM news where id={}".format(number))
    row_headers=[x[0] for x in mycursor.description]
    myresult = mycursor.fetchall()
    json_data=[]
    for result in myresult:
        json_data.append(dict(zip(row_headers,result)))
    return json_data

def getNewsByUser(userName):
    json_data=[]
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM users where user_name='{}'".format(userName))
    myresult = mycursor.fetchone()  
    mycursor.execute("SELECT id,source_url,source_name,claim,claim_urls,label,publish_date,author FROM news where id={}".format(myresult[1]))
    row_headers=[x[0] for x in mycursor.description]
    myresult = mycursor.fetchall()
    for result in myresult:
        json_data.append(dict(zip(row_headers,result)))
    return json_data

def addUserBelif(newsid,userName,userBeliev,userKnowledge):
    query="insert into newsdata (id,user_name,believ_index,prior_knowledge) values ({0},'{1}',{2},{3})".format(newsid,userName,userBeliev,userKnowledge);
    mycursor = mydb.cursor()
    print(query)
    mycursor.execute(query);
    mydb.commit()
    return mycursor.rowcount
    
def getUsersLastId(userName):
    if isUserAvailable(userName):
        mycursor = mydb.cursor()
        mycursor.execute("Update users where user_name='{}'".format(userName))
        myresult = mycursor.fetchone()
        return myresult[1]
    else:
        return -1

def updateUsersLastId(newsid,userName):
    print(newsid,":",isNewsAvailable(newsid), " " ,userName,":",isUserAvailable(userName))
    if isNewsAvailable(newsid) and isUserAvailable(userName):
        mycursor = mydb.cursor()
        mycursor.execute("update users set last_id={0} where user_name='{1}'".format(newsid,userName))
        print("update users set last_id={0} where user_name='{1}'".format(newsid,userName))
        mydb.commit()
        return True
    else:
        return False

def addNews(jsonlist):
    mycursor = mydb.cursor()
    for p in jsonlist:
        url=p['url']
        source=p['source']
        claim=p['claim']
        claim_url=p['claim_url']
        label=p['label']
        date=p['date']
        author=p['author']
        body="".join(p['body'])
        head="".join(p['head'])
        sql1="insert into news(source_url,source_name,claim,claim_urls,label,publish_date,author,content,bodycontent) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        mycursor.execute(sql1,(url,source,claim,claim_url,label,date,author,body,head))
        
        
    mydb.commit()
    return mycursor.rowcount

def addOneNews(p):
    mycursor = mydb.cursor()
    
    url=p['url']
    source=p['source']
    claim=p['claim']
    claim_url=p['claim_url']
    label=p['label']
    date=p['date']
    author=p['author']
    body="".join(p['body'])
    sql1="insert into news(source_url,source_name,claim,claim_urls,label,publish_date,author,content) values(%s,%s,%s,%s,%s,%s,%s,%s)"
    mycursor.execute(sql1,(url,source,claim,claim_url,label,date,author,body))
        
        
    mydb.commit()
    return mycursor.rowcount