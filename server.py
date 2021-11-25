from flask import Flask
from flask_restful import Resource, Api, reqparse
import ast

app = Flask(__name__)
api = Api(app)

class Test(Resource):
    def get(self):
        return {'message': "Welcome to the ArcadeScores API."}, 200

class Register(Resource):
    pass

class Login(Resource):
    pass

class Scores(Resource):
    pass

api.add_resource(Test,"/")
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Scores, '/scores')

if __name__ == '__main__':
    print('Server Started...')
    app.run()
