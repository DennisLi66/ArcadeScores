from flask import Flask #pip install flask
from flask_restful import Resource, Api, reqparse #pip install flask_restful

from formConnectionModule import formConnection
import bcrypt
import string
import random

class Login(Resource):
    def post(self): #Login to an Account
        parser = reqparse.RequestParser();
        parser.add_argument('email',required=True);
        parser.add_argument('password',required=True);
        args = parser.parse_args();
        try:
            connection = formConnection();
            query = "SELECT * FROM users WHERE email = %s;"
            cursor = connection.cursor(prepared = True);
            cursor.execute(query,(args['email']));
            connection.commit();
            results = cursor.fetchall();
            if (results.length == 0):
                connection.close();
                return {'status':-1,'message':'No Such Account.'}
            else:
                print(results);
                connection.close();
                return results;
            
        except:
            raise ValueError('Querying Failed.'); 



if __name__ == '__main__':
    print("Login Endpoint...")
