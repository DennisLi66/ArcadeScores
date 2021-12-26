from flask import Flask #pip install flask
from flask_restful import Resource, Api, reqparse #pip install flask_restful

import os
from dotenv import load_dotenv
import smtplib, ssl
import string
import random

from formConnectionModule import formConnection

class ForgotPassword(Resource):
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
            if (cursor.rowcount != 0):
                load_dotenv();
                EMAILUSER = os.getenv('EMAILUSER');
                EMAILPASSWORD = os.getenv('EMAILPASSWORD');
                subject = "Forgotten Password Recovery Code";
                body = """Your recovery code is %s.""" % (code)
                emailText = message = 'Subject: {}\n\n{}'.format(subject,body)
                smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465);
                smtp_server.ehlo();
                smtp_server.login(EMAILUSER, EMAILPASSWORD);
                smtp_server.sendmail(EMAILUSER, args['email'], emailText);
                smtp_server.close();
            return {'status':0, "message": "Recovery Email Sent."};
        except Exception as e:
            return {'message': str(e), 'status': -1}; 
        
if __name__ == '__main__':
    print("Forgot Password Endpoint...");
