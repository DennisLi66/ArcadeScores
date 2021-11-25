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
    def get(self):
        return {'message': "Welcome to the ArcadeScores API."}, 200

class Register(Resource):
    def post(self):
        return;

class Login(Resource):
    def post(self):
        return;

class Scores(Resource):
    def get(self):
        return;

class Times(Resource):
    def get(self):
        return;

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
