from flask import Flask #pip install flask
from flask_restful import Resource, Api, reqparse #pip install flask_restful

from formConnectionModule import formConnection

class ForgotPasswordCode(Resource):
    def post(self):
        parser = reqparse.RequestParser();
        parser.add_argument('code',required=True);
        parser.add_argument('email',required=True);
        args = parser.parse_args();
        try:
            connection = formConnection();
            query = """
            SELECT * FROM forgottenPasswordCodes WHERE email = %s AND fcode = %s
            """
            cursor = connection.cursor(prepared = True);
            cursor.execute(query,(args['email'],args['code']));
            res = cursor.fetchall();
            connection.commit();
            connection.close();
            if not res:
                return {'status':-2,"message":"Bad Match"}
            else:
                return {'status':0,"message": "Match"}        
        except Exception as e:
            return {'message': str(e), 'status': -1}; 
        
if __name__ == '__main__':
    print("Forgot Password Code Endpoint...");
