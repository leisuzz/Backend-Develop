import flask
import sqlite3
from flask import request, jsonify
from databasehelper import initDB
from extractdata import extractActionToData, extractUserToData

app = flask.Flask(__name__)
app.config["DEBUG"] = True
db_path = 'database/sqlite.db'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#default page
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Open House AI Demo </h1>'''

@app.errorhandler(400)
def bad_request(e):
    return "<h1>400</h1><p>Bad request. Make sure your params are correct.</p>", 400

#get all users and sessions, for testing 
@app.route('/api/v1/resources/user/all', methods=['GET'])
def api_users_all():
    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    res = cur.execute('SELECT * FROM user;').fetchall()
    conn.commit()
    cur.close()
    return jsonify(res)

#insert user and session, for front end
@app.route('/api/v1/resources/user', methods=['POST'])
def api_user():
    query_parameters = request.args
    
    id = query_parameters.get('id')
    sessionId = query_parameters.get('sessionId')

    if not (id or sessionId):
        return bad_request(400)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    try:
        sqlite_insert_with_param  = """ INSERT INTO user 
                    (id, sessionId)
                    VALUES 
                    (?, ?)"""
        data_tuple = (id, sessionId)
        cur.execute(sqlite_insert_with_param, data_tuple)
        conn.commit()
        cur.close()
    except Exception as e:
        return bad_request(400)
        print(e)

    return(jsonify(success=True))    

#get all actions, for testing
@app.route('/api/v1/resources/actions/all', methods=['GET'])
def api_actions_all():
    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    res = cur.execute('SELECT * FROM action;').fetchall()
    conn.commit()
    cur.close()
    return jsonify(res)

#insert action, for front end
@app.route('/api/v1/resources/actions', methods=['POST'])
def api_action():
    query_parameters = request.args
    
    user_sessionId = query_parameters.get('user_sessionId')
    type_text = query_parameters.get('type')
    locationX = query_parameters.get('locationX')
    locationY = query_parameters.get('locationY')
    viewedId = query_parameters.get('viewedId')
    pageFrom = query_parameters.get('pageFrom')
    pageTo = query_parameters.get('pageTo')

    if not (user_sessionId):
        return bad_request(400)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    try:
        sqlite_insert_with_param  = """ INSERT INTO action 
                    (user_sessionId, type, locationX, locationY, viewedId, pageFrom, pageTo)
                    VALUES 
                    (?, ?, ?, ?, ?, ?, ?)"""
        data_tuple = (user_sessionId, type_text, locationX, locationY, viewedId, pageFrom, pageTo)
        cur.execute(sqlite_insert_with_param, data_tuple)
        conn.commit()
        cur.close()
    except Exception as e:
        return bad_request(400)
        print(e)

    return(jsonify(success=True))  

#log dump
@app.route('/api/v1/resources/logdump', methods=['GET'])
def logdump():
    query_parameters = request.args
    
    userId = query_parameters.get('userId')
    lowerTimeRange = query_parameters.get('lowerTimeRange')
    upperTimeRange = query_parameters.get('upperTimeRange')
    logType = query_parameters.get('logType')

    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    cur = conn.cursor()

    query = "SELECT * FROM user"
    to_filter = []
    
    if userId:
        query += " WHERE id = ?"
        to_filter.append(userId)

    query += ";"
    dictOfUsers = cur.execute(query, to_filter).fetchall()

    jsoncollection = []

    for i in dictOfUsers:
        queryUserId = i['id']
        querySessionId = i['sessionId']
        
        to_filter = []
        countQuery = "SELECT COUNT(type) FROM action WHERE user_sessionId = ?"
        query = "SELECT * FROM action WHERE user_sessionId = ?"
        to_filter.append(querySessionId)

        if logType:
            countQuery += " AND type = ?"
            query += " AND type = ?"
            to_filter.append(logType)

        if lowerTimeRange:
            countQuery += " AND time >= ?"
            query += " AND time >= ?"
            to_filter.append(lowerTimeRange)

        if upperTimeRange:
            countQuery += " AND time < ?"
            query += " AND time < ?"
            to_filter.append(upperTimeRange)        

        countQuery += ";"
        countActions = cur.execute(countQuery, to_filter).fetchall()
        queryActions = cur.execute(query, to_filter).fetchall()

        if countActions[0]['COUNT(type)'] > 0:
            jsondata = extractUserToData(queryUserId, querySessionId)
            for j in queryActions:
                actiondata = extractActionToData(j)
                jsondata['actions'].append(actiondata)

            jsoncollection.append(jsondata)

    conn.commit()
    cur.close()
    return jsonify(jsoncollection)

initDB(db_path)
app.run()