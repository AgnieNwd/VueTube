from flask_httpauth import HTTPBasicAuth
from flask import abort, make_response
from flask_restful import Resource,  reqparse
from flask_jsonpify import jsonify
from datetime import datetime, timedelta
import logging, error, include


auth = HTTPBasicAuth()

class Authentification(Resource):
    def post(self):
        global directly_id
        auth = reqparse.RequestParser()
        auth.add_argument('username', type=str, required=True)
        auth.add_argument('password', type=str, required=True)
        args = auth.parse_args()

        usern = args['username']
        passwd = args['password']
        directly_id = str(include.authen(usern, passwd))
        if directly_id != "0" and error.tchek_token_expiration(directly_id) == True:
            user_token = include.create_token()
            include.add_token(user_token, directly_id)
        else:
            user_token = include.get_token_by_user(directly_id)
        data = include.get_user_by_id(directly_id)
        if data != False:
            return make_response(jsonify({"Message": 'OK', 'data': {'token': user_token, 'user': data}}), 201)
        else:
            return error.badRequest(10002, "Identifiant ou mot de passe invalide !")