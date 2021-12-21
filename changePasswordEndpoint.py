from flask import Flask #pip install flask
from flask_restful import Resource, Api, reqparse #pip install flask_restful

from formConnectionModule import formConnection
import string
import random

class ChangePassword(Resource):
    def post(self):
        print();
        
if __name__ == '__main__':
    print("Change Password Endpoint...");
