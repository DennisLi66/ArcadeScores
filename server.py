from flask import Flask #pip install flask
from flask_restful import Resource, Api, reqparse #pip install flask_restful
import os
from dotenv import load_dotenv #pip install python-dotenv
import ast
import mysql.connector #pip install mysql-connector-python

from formConnectionModule import formConnection
from scoresEndpoint import Scores
from timesEndpoint import Times
from sessionsEndpoint import Sessions

app = Flask(__name__)
api = Api(app)

class Test(Resource):
    def get(self): #Just for Testing Connection
        return {'message': "Welcome to the ArcadeScores API."}, 200

class Login(Resource):
    def post(self): #Login to an Account
        return;


api.add_resource(Test,"/")
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Scores, '/scores')
api.add_resource(Times, '/times')
api.add_resource(Sessions, '/sessions')

if __name__ == '__main__':
    print('Server Started...')
    connection = formConnection();
    connection.close();
    print('Connection Tested And Closed.');
    app.run()
