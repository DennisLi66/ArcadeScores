from flask import Flask #pip install flask
from flask_restful import Resource, Api, reqparse #pip install flask_restful
from flask_cors import CORS, cross_origin #pip install -U flask-cors
import os
from dotenv import load_dotenv #pip install python-dotenv
import ast
import mysql.connector #pip install mysql-connector-python

from formConnectionModule import formConnection
from scoresEndpoint import Scores
from timesEndpoint import Times
from sessionsEndpoint import Sessions
from registerEndpoint import Register
from loginEndpoint import Login
from forgotPasswordEndpoint import ForgotPassword
from forgotPasswordCodeEndpoint import ForgotPasswordCode
from changePasswordEndpoint import ChangePassword
from scoresWithTimesEndpoint import ScoresWithTimes

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'
@app.route("/")
# @cross_origin()
class Test(Resource):
    def get(self): #Just for Testing Connection
        return {'message': "Welcome to the ArcadeScores API."}, 200

api.add_resource(Test,"/") #Local Tested
api.add_resource(Register, '/register') #Local Tested
api.add_resource(Login, '/login') 
api.add_resource(Scores, '/scores')
api.add_resource(Times, '/times')
api.add_resource(Sessions, '/sessions')
api.add_resource(ForgotPassword, '/forgotpassword') #Local Tested
api.add_resource(ForgotPasswordCode, '/forgotpasswordcode') #Local Tested
api.add_resource(ChangePassword, '/changepassword'); #Local Tested
api.add_resource(ScoresWithTimes, '/scoreswithtimes');

if __name__ == '__main__':
    print('Server Started...')
    connection = formConnection();
    connection.close();
    print('Connection Tested And Closed.');
    app.run()
