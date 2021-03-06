from flask import Flask #pip install flask
from flask_restful import Resource, Api, reqparse #pip install flask_restful

from formConnectionModule import formConnection
from checkSessionsFunction import checkSession

class Scores(Resource):
    def get(self): #Return all scores, or a specified group
        parser = reqparse.RequestParser();
        parser.add_argument('userID',required=False);
        parser.add_argument('gameID',required=True);
        args = parser.parse_args();
        try:
            connection = formConnection();
            query = "SELECT username, score, DATE_FORMAT(submissionTime, '%Y-%m-%d %T.%f') FROM scores LEFT JOIN users ON users.userID = scores.userID WHERE gameID = %s";
            variables = (args['gameID'],);
            if (args['userID']):
                query += " AND userID = %s ORDER BY score DESC";
                variables = (args['gameID'],args['userID']);
            else:
                query += " ORDER BY score DESC";
            cursor = connection.cursor(prepared=True);
            cursor.execute(query,variables);
            res = cursor.fetchall(); 
            connection.close();
            return {'status':0,'results':res}
        except Exception as e:
            return {'message': str(e), 'status': -1}; 
         
    def put(self): #Add new score #Will Need Session Checking Later
        parser = reqparse.RequestParser();
        parser.add_argument('userID',required=True);
        parser.add_argument('score',required=True);
        parser.add_argument('gameID',required=True);
        parser.add_argument('sessionID',required=True);
        args = parser.parse_args();
        if (checkSession(args['userID'],args['sessionID']) == False):
            return {'status':-2,'message':'Session Expired'}
        try:
            connection = formConnection();
            query = "INSERT INTO scores (userID,gameID,score,submissionTime) VALUES (%s,%s,%s,NOW())";
            cursor = connection.cursor(prepared=True);
            cursor.execute(query,(args['userID'],args['gameID'],args['score']))
            connection.commit();
            connection.close();
        except Exception as e:
            return {'message':str(e),'status':-1}
        return {'message':'Put Request Transaction Occured Successfully.'}, 200;

if __name__ == '__main__':
    print('Scores Endpoint...')
