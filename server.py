from flask import Flask #pip install flask
from flask_restful import Resource, Api, reqparse #pip install flask_restful
import os
from dotenv import load_dotenv #pip install python-dotenv
import ast
import mysql.connector #pip install mysql-connector-python

from formConnectionModule import formConnection


app = Flask(__name__)
api = Api(app)

class Test(Resource):
    def get(self): #Just for Testing Connection
        return {'message': "Welcome to the ArcadeScores API."}, 200

class Register(Resource):
    def post(self):  #Register a New Account
        return;

class Login(Resource):
    def post(self): #Login to an Account
        return;

class Session(Resource):
    def post(self): #Check Session Valid
        parser = reqparse.RequestParser();
        parser.add_argument('userID',required=True);
        parser.add_argument('sessionID',required=True);
        args = parser.parse_args();
        try:
            connection = formConnection();
            query = """
            SELECT * FROM sessions
            RIGHT JOIN
            (select userID,max(sessionDate) as high from sessions group by userID) highDates
            ON highDates.userID = sessions.userID
            WHERE userID = %s AND sessionID = %s
            AND ((timeDuration = 'forever')
            OR (timeduration = "HOUR" AND NOW() < date_add(sessionDate,Interval 1 Hour)))
            """;
            cursor = connection.cursor(prepared=True);
            cursor.execute(query,(args['userID'],args['sessionID']));
            connection.commit();
            results = cursor.fetchall();
            connection.close();
            print(results);
            return results;
        except:
            raise ValueError('Querying Failed');
    def patch(self): #Update Session
        return;
    def delete(self): #Expire Session 
        return; 

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

api.add_resource(Test,"/")
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Scores, '/scores')
api.add_resource(Times, '/times')

if __name__ == '__main__':
    print('Server Started...')
    connection = formConnection();
    connection.close();
    print('Connection Tested And Closed.');
    app.run()
