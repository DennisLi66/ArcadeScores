from flask import Flask #pip install flask
from flask_restful import Resource, Api, reqparse #pip install flask_restful

from formConnectionModule import formConnection

class ScoresWithTimes(Resource):
    def get(self):
        parser = reqparse.RequestParser();
        parser.add_argument('sortBy',required = True);
        parser.add_argument('userID',required = False);
        parser.add_argument('gameID',required = True);
        args = parser.parse_args();
        try:
            connection = formConnection();
            sortByMethod = "";
            selectFromMethod = "SELECT * FROM scoreOverTimes WHERE gameID = %s";
            variables = (args['gameID']);
            if (args['sortBy'] == "recent"):
                sortByMethod = " ORDER BY submissionTime DESC";
            elif (args['sortBy'] == "top"):
                sortByMethod = " ORDER BY score DESC, timeInMilliseconds ASC";
            else:
                return {'message': "Sort By Choice Invalid.", 'status':-1};
            if (args['userID']):
                selectFromMethod = "SELECT * FROM scoreOverTimes WHERE gameID = %s AND userID = %s";
                variables = (args['gameID'],args['userID']);
            query = selectFromMethod + sortByMethod;
            cursor = connection.cursor(prepared=True);
            cursor.execute(query,variables);
            res = cursor.fetchall(); 
            connection.commit();
            connection.close();
            return {'status':0,'results':res};
        except Exception as e:
            return {'message': str(e), 'status': -1}; 
            
    def put(self):
        return;
    
