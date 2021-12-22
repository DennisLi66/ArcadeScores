from flask import Flask #pip install flask
from flask_restful import Resource, Api, reqparse #pip install flask_restful
import bcrypt

from formConnectionModule import formConnection
import string
import random

class ChangePassword(Resource):
    def post(self):
        # Need code with email and a new password or a new password
        # with email and session
        parser = reqparse.RequestParser();
        parser.add_argument('password',required=True);
        parser.add_argument('email',required=True);
        parser.add_argument('sessionID',required=False);
        parser.add_argument('code',required=False);
        args = parser.parse_args();
        try:
            if args['sessionID'] and args['code']:
                return {'status':-1,'message':'Impossible Circumstance.'}
            else if args['sessionID']:
                #NEEDS WORK LATER
            else if args['code']:
                uQuery = """
                UPDATE users SET salt = %s, passcode = %s WHERE
                (%s, %s) IN (SELECT email,fcode FROM forgottenPasswordCodes)
                 """
                dQuery = """
                DELETE FROM forgottenPasswordCodes WHERE fcode = %s AND email = %s;
                """
                salt = bcrypt.gensalt(); #need to store salt too
                hashPass = bcrypt.hashpw(args['password'].encode('utf-8'),salt)
                cursor = connection.cursor(prepared = True);
                cursor.execute(uQuery,(salt,hashPass,args['email'],args['code']));
                if (cursor.rowcount == 0):
                    return {'status':0,message:"No Updates."}
                cursor = connection.cursor(prepared = True);
                cursor.execute(dQuery,(args['code'],args['email']));
                return {'status':0,message: "Update Occurred."}
            else:
                return {'status:'-1,'message':'Not Enough Information'}
        except Exception as e:
            return {'message': str(e), 'status': -1};       
        
if __name__ == '__main__':
    print("Change Password Endpoint...");
