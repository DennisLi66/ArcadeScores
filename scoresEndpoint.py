from flask import Flask #pip install flask
from flask_restful import Resource, Api, reqparse #pip install flask_restful

from formConnectionModule import formConnection


class Scores(Resource):
    def get(self): #Return all scores, or a specified group
        return;
    def put(self): #Add new score #Will Need Session Checking Later
        parser = reqparse.RequestParser();
        parser.add_argument('userID',required=True);
        parser.add_argument('score',required=True);
        parser.add_argument('gameID',required=True);
        args = parser.parse_args();
        try:
            connection = formConnection();
            query = "INSERT INTO scores (userID,gameID,score,submissionTime) VALUES (%s,%s,%s,NOW())";
            cursor = connection.cursor(prepared=True);
            cursor.execute(query,(args['userID'],args['gameID'],args['score']))
            connection.commit();
            connection.close();
        except:
            raise ValueError('Querying Failed.')
        return {'message':'Put Request Transaction Occured Successfully.'}, 200;

if __name__ == '__main__':
    print('Scores Endpoint...')
