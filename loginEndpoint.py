from flask import Flask #pip install flask
from flask_restful import Resource, Api, reqparse #pip install flask_restful

from formConnectionModule import formConnection
from makeSessionModule import makeSession
import bcrypt
import string
import random

class Login(Resource):
    def post(self): #Login to an Account
        parser = reqparse.RequestParser();
        parser.add_argument('email',required=True);
        parser.add_argument('password',required=True);
        parser.add_argument('timeDuration',required=True);
        args = parser.parse_args();
        try:
            connection = formConnection();
            cursor = connection.cursor(prepared = True);
            cursor.execute("SELECT * FROM users WHERE email = %s;",[args['email']]);
            results = cursor.fetchall();
            if (len(results) == 0):
                connection.close();
                return {'status':-1,'message':'No Such Account.'}
            else:
                hashPass = "";
                salt = "";
                userID = 0;
                for row in results:
                    salt = row[3];
                    userID = row[0];
                    name = row[1];
                    hashPass = row[4];
                if bcrypt.checkpw(args['password'].encode('utf-8'),hashPass.encode('utf-8')):
                    sessionSequence = makeSession(userID,args['timeDuration']);
                    connection.close();
                    return {'status': 0, 'userID': userID , 'sessionID':sessionSequence, 'name':name};
                else:
                    connection.close();
                    return {'status': -1, 'message':'No Matches'}, 200
            
        except Exception as e:
            return {'status': -1, 'message': str(e)}, 200



if __name__ == '__main__':
    print("Login Endpoint...")
