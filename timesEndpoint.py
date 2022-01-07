from flask import Flask #pip install flask
from flask_restful import Resource, Api, reqparse #pip install flask_restful

from formConnectionModule import formConnection
from checkSessionsFunction import checkSession

class Times(Resource):
    def get(self): #Return all scores, or a specified group
        parser = reqparse.RequestParser();
        parser.add_argument('userID',required=False);
        parser.add_argument('gameID',required=True);
        args = parser.parse_args();
        try:
            connection = formConnection();
            query = "";
            if (args['userID']):
                query = "SELECT * FROM times WHERE gameID = %s AND userID = %s ORDER BY timeInMilliseconds ASC";
                cursor = connection.cursor(prepared=True);
                cursor.execute(query,(args['gameID'],args['userID']));
            else:
                query = "SELECT * FROM times WHERE gameID = %s ORDER BY timeInMilliseconds ASC";
                cursor = connection.cursor(prepared=True);
                cursor.execute(query,(args['gameID']));
            res = cursor.fetchall(); 
            connection.commit();
            connection.close();
            return {'status':0,'results':res}
        except Exception as e:
            return {'message': str(e), 'status': -1}; 
    def put(self): #Add a new score #Will need session checking later
        parser = reqparse.RequestParser();
        parser.add_argument('userID',required=True);
        parser.add_argument('gameID',required=True);
        parser.add_argument('timeInMilliseconds',required=True); #Caps at around 1000000000 milliseconds, or a little more than a week
        parser.add_argument('sessionID',required=True);
        args = parser.parse_args();
        if (checkSession(args['userID'],args['sessionID']) == False):
            return {'status':-2,'message':'Session Expired'}
        try:
            connection = formConnection();
            query = "INSERT INTO times (userID,gameID,timeInMilliseconds,submissionTime) VALUES (%s,%s,%s,NOW())";
            cursor = connection.cursor(prepared = True);
            cursor.execute(query,(args['userID'],args['gameID'],args['timeInMilliseconds']));
            connection.commit();
            connection.close();
        except Exception as e:
            return {'message':e,'status':-1}
        return {'message': "Put Request Transaction Occured Successfully."}, 200;


if __name__ == '__main__':
    print("Times Endpoint...")
