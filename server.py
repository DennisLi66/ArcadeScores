from flask import Flask #pip install flask
from flask_restful import Resource, Api, reqparse #pip install flask_restful
import os
from dotenv import load_dotenv #pip install python-dotenv
import ast
import mysql.connector #pip install mysql-connector-python

app = Flask(__name__)
api = Api(app)

def formConnection():
    try:
        load_dotenv()
        conn = mysql.connector.connect(
            host=os.getenv('SQLHOST'),
            user=os.getenv('SQLUSER'),
            password=os.getenv('SQLPASSWORD'),
            database=os.getenv('SQLDATABASE')
            )
        return conn;        
    except:
        raise ValueError("There was no .env file or .env variables, or connection failed.")


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
    def get(self): #Check Session Valid
        return;
    def patch(self): #Update Session
        return;
    def delete(self): #Delete Session
        return; 

class Scores(Resource):
    def get(self): #Return all scores, or a specified group
        return;
    def put(self): #Add new score
        return;

class Times(Resource):
    def get(self): #Return all scores, or a specified group
        return;
    def put(self): #Add a new score
        parser = reqparse.RequestParser();
        parser.add_argument('userID',required=True);
        parser.add_argument('timeInMilliseconds',required=True); #Caps at around 1000000000 milliseconds, or a little more than a week
        args = parser.parse_args();
        print(args)
        try:
            connection = formConnection();
            query = "INSERT INTO times (userID,timeInMilliseconds,submissionTime) VALUES (%s,%s,NOW())";
            cursor = connection.cursor(prepared = True);
            cursor.execute(query,(args['userID'],args['timeInMilliseconds']));
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
