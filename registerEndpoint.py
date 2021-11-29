from flask import Flask #pip install flask
from flask_restful import Resource, Api, reqparse #pip install flask_restful

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
            connection = formConnection();
            salt = bcrypt.gensalt(); #need to store salt too
            hashPass = bcrypt.hashpw(args['password'].encode('utf8'),salt)
            print(hashPass)
            query = """
            INSERT INTO users (username,email,salt,passcode) VALUES
            (%s,%s,%s,%s)
            """
            cursor = connection.cursor(prepared = True);
            cursor.execute(query,(args['username'],args['email'],salt,hashPass));
            connection.commit();
            connection.close();
        except:
            raise ValueError('Querying Failed.');
        return {'message': "Post Request Transaction Occured Successfully."}, 200;

            
if __name__ == '__main__':
    print("Registration Endpoint...")
