from flask import Flask #pip install flask
from flask_restful import Resource, Api, reqparse #pip install flask_restful
import mysql.connector #pip install mysql-connector-python

from formConnectionModule import formConnection
import bcrypt


class Register(Resource):
    def post(self):  #Register a New Account
        parser = reqparse.RequestParser();
        parser.add_argument('email',required=True);
        parser.add_argument('password',required=True);
        parser.add_argument('username',required=True);
        args = parser.parse_args();
        try:
            try:
                connection = formConnection();
            except:
                raise ValueError("MYSQL Connection Failed.")
            salt = bcrypt.gensalt(); #need to store salt too
            hashPass = bcrypt.hashpw(args['password'].encode('utf-8'),salt)
            print(hashPass)
            query = """
            INSERT INTO users (username,email,salt,passcode) VALUES
            (%s,%s,%s,%s)
            """
            cursor = connection.cursor(prepared = True);
            cursor.execute(query,(args['username'],args['email'],salt,hashPass));
            connection.commit();
            connection.close();
        except mysql.connector.Error:
            return {'status':-1,'message':'This email is already registered.'},200
        except Exception as e:
            return {'status':-1,'message':str(e)}
        return {'status':0,'message': "Post Request Transaction Occured Successfully."}, 200;

            
if __name__ == '__main__':
    print("Registration Endpoint...")
