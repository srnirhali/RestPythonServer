from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
import Databasecon as db
import datetime
import json
import scrapper as scrap
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="cat@123",
      database="newsdatabase"
    )


with open(r'C:\Users\Dell\OneDrive\Documents\sample.json') as json_file:
    data = json.load(json_file)
    for p in data:
        print('claim: ' + p['claim'])

def default_date(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()

@app.route('/getallnewsdb/',methods=['GET'])
def getAllNewsDB():
    jsonfinal=(json.dumps(db.getAllNewsDB(),indent=4,default=default_date))
    resp = Response(jsonfinal, status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
    

@app.route('/getallnews/',methods=['GET'])
def getAllNews():
    return jsonify(data)

@app.route('/getnews/<number>',methods=['GET'])
def getNewsByNumber(number):
    jsonfinal=(json.dumps(db.getNewsByID(int(number)),indent=4,default=default_date))
    resp = Response(jsonfinal, status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
    

@app.route('/getnewsbyuser/<user>',methods=['GET'])
def getNewsByUser(user):
    if db.isUserAvailable(user):
        jsonfinal=(json.dumps(db.getNewsByUser(user),indent=4,default=default_date))
        resp = Response(jsonfinal, status=200, mimetype='application/json')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    else:
        resp = Response("{'Message':'No User Available'}", status=404, mimetype='application/json')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    


@app.route('/adduserbeliev',methods=['POST'])
def addUserBeliev(): 
    if request.method == 'POST':  
        newsid = int(request.form.get('id'))
        userName=request.form.get('username')
        userBeliev=int(request.form.get('userbeliev'))
        userKnowledge=int(request.form.get('userknowledge'))
        print(newsid,userName,userBeliev,userKnowledge)
        count = db.addUserBelif(newsid,userName,userBeliev,userKnowledge)
        if count == 0:
            resp = Response("{'Message':'Data is Not updated'}", status=500, mimetype='application/json')
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        else:
            nextid= newsid+1
            print(nextid)
            if db.updateUsersLastId(nextid,userName):
                return getNewsByUser(userName)
            else:
                resp = Response("{'Message':'No more news'}", status=404, mimetype='application/json')
                resp.headers['Access-Control-Allow-Origin'] = '*'
                return resp

@app.route('/getuser',methods=['POST'])
def getUserDetails(): 
    if request.method == 'POST':  #this block is only entered when the form is submitted
        userName=request.form.get('username')
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM users where user_name='{}'".format(userName))
        row_headers=[x[0] for x in mycursor.description]
        myresult = mycursor.fetchall()
        if mycursor.rowcount==0:
            mycursor.execute("insert into users(user_name,last_id) values('{}',1) ".format(userName))
            mydb.commit();
        mycursor.execute("SELECT * FROM users where user_name='{}'".format(userName))
        row_headers=[x[0] for x in mycursor.description]
        myresult = mycursor.fetchall()
        json_data=[]
        for result in myresult:
            json_data.append(dict(zip(row_headers,result)))
        jsonfinal=(json.dumps(json_data,indent=4,default=default_date))
        resp = Response(jsonfinal, status=200, mimetype='application/json')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    
    return jsonify({'result': 'true'}), 201

@app.route('/getuser/<username>',methods=['GET'])
def getUserDetailsByURL(username):
    data=db.getUserDetails(username)
    if data is not None:
        jsonfinal=(json.dumps(data,indent=4,default=default_date))
        resp = Response(jsonfinal, status=200, mimetype='application/json')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    else:
        resp = Response("{'Message':'No User Available'}", status=404, mimetype='application/json')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
        
@app.route('/createuser/<username>',methods=['GET'])
def createUser(username):
    if db.isUserAvailable(username):
        resp = Response("{'Message':'User Name is already Available'}", status=406, mimetype='application/json')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    else:
        count=db.createUser(username)
        if count == 0:
            resp = Response("{'Message':'User Not created Available'}", status=406, mimetype='application/json')
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        else:
            return getUserDetailsByURL(username)
        
        
@app.route('/uploadjson',methods=['POST'])
def uploadJsonFile():
    #newsid = str(request.files['document'].read(), 'utf-8')
    posted_data = json.load(request.files['document'])
    
    for index,data in enumerate( posted_data,start=0):
        body,title = scrap.getAllPAndTitleTagsFormPage(data['url'],title=True)
        #data['body']= body
        paragraphs = []
        for x in body:
            paragraphs.append(str(x))
        
        titleparagraphs = []
        for x in title:
            titleparagraphs.append(str(x))
        
        #print("".join(titleparagraphs))
        posted_data[index]["body"]= paragraphs
        posted_data[index]["head"]= titleparagraphs
        #print(posted_data[index]," " ,index)
        
    count=db.addNews(posted_data)
    
    if count == 0:
        resp = Response("{'Message':'Not Inserted'}", status=406, mimetype='application/json')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    else:
        resp = Response("{'Message':'Data Is Inserted'}", status=200, mimetype='application/json')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    
@app.route('/test',methods=['GET'])
def getSourceFromURL():
    url="https://twitter.com/GOPLdrBrianKolb/status/1176577065291780097?s=20"
    data = url.split('/')
    print(data[3:4])    

if __name__ == '__main__':
 app.run()