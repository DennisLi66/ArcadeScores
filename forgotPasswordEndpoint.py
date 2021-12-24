from flask import Flask #pip install flask
from flask_restful import Resource, Api, reqparse #pip install flask_restful

import os
from dotenv import load_dotenv
import smtplib

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
            #EMAIL SENT HERE
            if (cursor.rowcount == 1):
                load_dotenv();
                EMAILUSER = os.getenv('EMAILUSER');
                EMAILPASSWORD = os.getenv('EMAILPASSWORD');
                subject = "Forgotten Password Code";
                body = "Your recovery code is %s." % (code)
                emailText = """\
                From: %s
                To: %s
                Subject: %s

                %s
                """ % (EMAILUSER,args['email'],subject,body);
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
