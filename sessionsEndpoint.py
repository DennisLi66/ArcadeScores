from flask import Flask #pip install flask
from flask_restful import Resource, Api, reqparse #pip install flask_restful

from formConnectionModule import formConnection

class Sessions(Resource):
    def patch(self): #Update Session
        parser = reqparse.RequestParser();
        parser.add_argument('userID',required=True);
        parser.add_argument('sessionID',required=True);
        args = parser.parse_args();
        try:
            connection = formConnection();
            query = """
            UPDATE sessions SET sessionDate = NOW()
            WHERE userID = %s AND sessionID = %s
            AND (sessionID in (select sessionID FROM (select userID,sessionID, max(sessionDate) from sessions group by userID)))
            AND (timeduration = "HOUR" AND NOW() < date_add(sessionDate,Interval 1 Hour)
            """;
            cursor = connection.cursor(prepared=True);
            cursor.execute(query,(args['userID'],args['sessionID']));
            connection.commit();
            connection.close();
            return {'status':0,'message':'Update Occured Successfully.'};  
        except Exception as e:
            return {'status':-1,'message':str(e)}
    def delete(self): #Expire Session
        parser = reqparse.RequestParser();
        parser.add_argument('userID',required=True);
        parser.add_argument('sessionID',required=True);
        args = parser.parse_args();
        try:
            connection = formConnection();
            query = """
            UPDATE sessions SET timeDuration = 'expired' WHERE
            userID = %s AND sessionID = %s
            """;
            cursor = connection.cursor(prepared=True);
            cursor.execute(query,(args['userID'],args['sessionID']));
            connection.commit();
            connection.close();
            return {'status':0,',message':'Delete Occured Successfully.'};       
        except Exception as e:
            return {'status':-1,'message':str(e)}
if __name__ == '__main__':
    print("Sessions Endpoint...")
