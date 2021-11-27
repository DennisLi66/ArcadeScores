from flask import Flask #pip install flask
from flask_restful import Resource, Api, reqparse #pip install flask_restful

from formConnectionModule import formConnection

class Sessions(Resource):
    def post(self): #Check Session Valid
        parser = reqparse.RequestParser();
        parser.add_argument('userID',required=True);
        parser.add_argument('sessionID',required=True);
        args = parser.parse_args();
        try:
            connection = formConnection();
            query = """
            SELECT * FROM sessions RIGHT JOIN
            (select userID,max(sessionDate) as high from sessions group by userID) highDates
            ON highDates.userID = sessions.userID
            WHERE userID = %s AND sessionID = %s
            AND ((timeDuration = 'forever')
            OR (timeduration = "HOUR" AND NOW() < date_add(sessionDate,Interval 1 Hour)))
            """;
            cursor = connection.cursor(prepared=True);
            cursor.execute(query,(args['userID'],args['sessionID']));
            connection.commit();
            results = cursor.fetchall();
            connection.close();
            print(results);
            return results;
        except:
            raise ValueError('Querying Failed');
    def patch(self): #Update Session
        return;
    def delete(self): #Expire Session
        parser = reqparse.RequestParser();
        parser.add_argument('userID',required=True);
        parser.add_argument('sessionID'required=True);
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
            results = cursor.fetchall();
            connection.close();
            print(results);
            return results;       
        except:
            raise ValueError('Querying Failed')
        return; 

if __name__ == '__main__':
    print("Sessions Endpoint...")
