from flask import jsonify, request
from flask_restful import Resource 
from vite.model import User
4



class Usuario(Resource):
    
    def get(self):
        user = User.query.all()
    
        return jsonify({"Users": [users.to_dict()for users in user]})





