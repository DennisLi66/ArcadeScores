from flask import Flask #pip install flask
from flask_restful import Resource, Api, reqparse #pip install flask_restful

from formConnectionModule import formConnection

class Times(Resource):
    def get(self): #Return all scores, or a specified group
        return;
    def put(self): #Add a new score #Will need session checking later
        parser = reqparse.RequestParser();
        parser.add_argument('userID',required=True);
        parser.add_argument('gameID',required=True);
        parser.add_argument('timeInMilliseconds',required=True); #Caps at around 1000000000 milliseconds, or a little more than a week
        args = parser.parse_args();
        try:
            connection = formConnection();
            query = "INSERT INTO times (userID,gameID,timeInMilliseconds,submissionTime) VALUES (%s,%s,%s,NOW())";
            cursor = connection.cursor(prepared = True);
            cursor.execute(query,(args['userID'],args['gameID'],args['timeInMilliseconds']));
            connection.commit();
            connection.close();
        except:
            raise ValueError('Querying Failed.')
        return {'message': "Put Request Transaction Occured Successfully."}, 200;


if __name__ == '__main__':
    print("Times Endpoint...")
