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
        parser.add_argument('timeDuration',required=True);
        args = parser.parse_args();
        try:
            connection = formConnection();
            cursor = connection.cursor(prepared = True);
            cursor.execute("SELECT * FROM users WHERE email = %s;",[args['email']]);
            #connection.commit();
            results = cursor.fetchall();
            if (len(results) == 0):
                connection.close();
                return {'status':-1,'message':'No Such Account.'}
            else:
                print(results);
                hashPass = "";
                salt = "";
                userID = ""; #Might Be Int //CHECK THIS
                for row in records:
                    salt = row[3];
                    userID = row[0];
                    #hashPass = row[4];
                #check password: if correct create sessionID and send back as result
                    #else go away
                #newHashPass = bcrypt.hashpw(args['password'],salt)
                if bcrypt.checkpw(args['password'],hashPass):
                    sessionSequence = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
                    insertSessionQuery = """
                    INSERT INTO sessions (sessionID,userID,sessionDate,timeDuration) VALUES (%s,%s,NOW(),%s)
                    """
                    cursor = connection.cursor(prepared = True);
                    cursor.execute(insertSessionQuery,[sessionSequence,userID,args['timeDuration']])
                    connection.close();
                    return {'status': 0, 'sessionID':sessionSequence};
                else:
                    connection.close();
                    return {'status': -1, 'message':'No Matches'}, 200
            
        except:
            raise ValueError('Querying Failed.'); 



if __name__ == '__main__':
    print("Login Endpoint...")
