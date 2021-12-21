from flask import Flask #pip install flask
from flask_restful import Resource, Api, reqparse #pip install flask_restful

from formConnectionModule import formConnection
import string
import random

class ChangePassword(Resource):
    def post(self):
        parser = reqparse.RequestParser();
        parser.add_argument('email',required=True);
        args = parser.parse_args();
        try:
            letters = string.digits + string.ascii_uppercase;
            code = ''.join(random.choice(letters) for i in range(10));
            connection = formConnection();
            #randomly generate a code
            query = """
            INSERT INTO forgottenPasswordCodes (email,fcode)
            SELECT email,%s FROM users WHERE email = %s
            ON DUPLICATE KEY UPDATE fcode = %s
            """
            cursor = connection.cursor(prepared=True);
            cursor.execute(query,(code,args['email'],code));
            connection.commit();
            connection.close();
            return {'status':0};
        except Exception as e:
            return {'message': str(e), 'status': -1}; 
        
if __name__ == '__main__':
    print("Change Password Endpoint...");
