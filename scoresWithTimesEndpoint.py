from flask import Flask #pip install flask
from flask_restful import Resource, Api, reqparse #pip install flask_restful

from formConnectionModule import formConnection
from checkSessionsFunction import checkSession
import json
import datetime


class ScoresWithTimes(Resource):
    def get(self):
        parser = reqparse.RequestParser();
        parser.add_argument('sortBy',required = True);
        parser.add_argument('userID',required = False);
        parser.add_argument('gameID',required = True);
        args = parser.parse_args();
        try:
            connection = formConnection();
            sortByMethod = "";
            selectFromMethod = """
            SELECT username, score, timeInMilliseconds, DATE_FORMAT(submissionTime, '%Y-%m-%d %T.%f') as timeframe FROM scoreOverTimes
            LEFT JOIN users ON users.userID = scoreOverTimes.userID
            WHERE gameID = %s
            """;
            variables = (args['gameID'],);
            if (args['userID']):
                selectFromMethod += "AND scoreOverTimes.userID = %s";
                variables = (args['gameID'],args['userID']);
            if (args['sortBy'] == "recent"):
                sortByMethod = " ORDER BY submissionTime DESC";
            elif (args['sortBy'] == "top"):
                sortByMethod = " ORDER BY score DESC, timeInMilliseconds ASC";
            else:
                return {'message': "Sort By Choice Invalid.", 'status':-1};
            query = selectFromMethod + sortByMethod;
            cursor = connection.cursor(prepared=True);
            cursor.execute(query,variables);
            res = cursor.fetchall(); 
            connection.commit();
            connection.close();
            return {'status':0,'results':res};
        except Exception as e:
            return {'message': str(e), 'status': -1}; 
            
    def put(self):
        parser = reqparse.RequestParser();
        parser.add_argument('userID',required=True);
        parser.add_argument('score',required=True);
        parser.add_argument('gameID',required=True);
        parser.add_argument('sessionID',required=True);
        parser.add_argument('timeInMilliseconds',required=True);
        args = parser.parse_args();
        if (checkSession(args['userID'],args['sessionID']) == False):
            return {'status':-2,'message':'Session Expired'}
        try:
            connection = formConnection();
            query = """
            INSERT INTO scoreOverTimes (userID,gameID,score,timeInMilliseconds,submissionTime)
            VALUES (%s,%s,%s,%s,NOW())
            """;
            cursor = connection.cursor(prepared = True);
            cursor.execute(query,(args['userID'],args['gameID'],args['score'],args['timeInMilliseconds']));
            connection.commit();
            connection.close();
        except Exception as e:
            return {'message':str(e),'status':-1}
        return {'message':'Put Request Transaction Occured Successfully.'}, 200;
    
