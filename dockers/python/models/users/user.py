import logging
from flask import request, make_response, jsonify
from flask_restful import Resource,  reqparse
from models.users import model as mod
import include
import error

user_schema = mod.UserSchema()
users_schema = mod.UserSchema(many=True)


class Users(Resource):

    # Get list of users
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('pseudo', type=str)
        parser.add_argument('page', type=str)
        parser.add_argument('perPage', type=str)
        args = parser.parse_args()

        _userPseudo = args['pseudo'] if args['pseudo'] else ''
        _page = int(args['page']) if args['page'] and args['page'] is not "0" and args['page'].isdigit() else 1
        _perPage = int(args['perPage']) if args['perPage'] and args['perPage'] is not "0" and args['perPage'].isdigit() else 50

        start_index = _perPage * _page - _perPage
        if _userPseudo != "":
            all_users = mod.User.query.filter(mod.User.pseudo.like('%' + _userPseudo + '%')).all()
        else:
            all_users = mod.User.query.all()
        result = users_schema.dump(all_users)
        result = result.data[start_index:start_index+_perPage]
        return make_response(jsonify({'Message ': 'OK', 'data': result, 'pager': {'current': _page, 'total': len(result)}}))


class User(Resource):
    def get_timestamp(self):
        return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

    # Get User by Id
    def get(self, user_id):
        if error.ifId(user_id) is False:
            return error.notFound()
        token_head = include.header()
        if include.get_user_id_by_token(token_head) == int(user_id):
            getUser = mod.User.query.get(user_id)
            data = user_schema.dump(getUser).data
        else:
            data = include.get_user_by_id(user_id)
        if data != False:
            return make_response(jsonify({'Message': 'OK', 'data': data}))
        else:
            return error.badRequest(10005, "erreur dans le traitement de la requête")

    # Update User by Id
    def put(self, user_id):
        if error.ifId(user_id) is False:
           return error.notFound()
        token_head = include.header()
        if error.ifToken(token_head) is True:
            if include.get_user_id_by_token(token_head) != int(user_id):
                return error.forbidden()
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str, help='Username to update user')
            parser.add_argument('email', type=str, help='Email address to update user')
            parser.add_argument('pseudo', type=str, help='Pseudo to update user')
            parser.add_argument('password', type=str, help='Password to update user')
            args = parser.parse_args()
            _userUsername = args['username']
            _userEmail = args['email']
            _userPseudo = args['pseudo']
            _userPassword = args['password']
            data = include.get_user_by_id(user_id)
            user = mod.User.query.get(user_id)
            stack = error.tchek_form_put_user(_userPassword, _userEmail, _userUsername, data['username'], data['email'] )
            if stack  != "":
                return error.badRequest(10034, stack)
            else:
                if _userUsername != "":
                    user.username = _userUsername
                if _userEmail != "":
                    user.email = _userEmail
                if _userPassword != "":
                    include.send_email("password", user.email, user.username)
                    user.password = _userPassword
                if _userPseudo != "":
                    user.pseudo = _userPseudo
            if user is not None:
                logging.info("Info logging: USER is NOT NONE")
                mod.db.session.commit()
                return self.get(user_id)
            else:
                logging.info("Info logging: User is NONE")
                return error.badRequest(10005, "erreur dans le traitement de la requête")
        else:
            return error.unauthorized()

    # Delete User by Id
    def delete(self, user_id):
        if error.ifId(user_id) is False:
           return error.notFound()
        token_head = include.header()

        logging.info("\n\nUSER_ID_token :: {} \n".format(include.get_user_id_by_token(token_head)))

        if error.ifToken(token_head) is True:
            if include.get_user_id_by_token(token_head) != int(user_id):
               return error.forbidden()
            include.delete_all_by_user_id(user_id)
            include.delete_token(user_id)
            user = mod.User.query.get(user_id)
            if user is not None:
                mod.db.session.delete(user)
                mod.db.session.commit()
                return {}, 204
            else:
                return error.badRequest(10005, "erreur dans le traitement de la requête")
        else:
            logging.info("TOKEN HEAD :: {}\n".format(token_head))
            logging.info("ifToken :: {}\n".format(error.ifToken(token_head)))
            return error.unauthorized()
    
class UserById(Resource):

    # Create user
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='Username to create user')
        parser.add_argument('email', type=str, help='Email address to create user')
        parser.add_argument('pseudo', type=str, help='Pseudo to create user')
        parser.add_argument('password', type=str, help='Password to create user')
        args = parser.parse_args()

        _userUsername = args['username']
        _userEmail = args['email']
        _userPseudo = args['pseudo']
        _userPassword = args['password']
        stack = str(error.tchek_username(_userUsername)) + str(error.tchek_email(_userEmail)) + str(
            error.tchek_password(_userPassword))
        logging.info("We are here, create user \n")
        if _userUsername and _userEmail and _userPassword is not None:
            if stack != "":
                logging.info(stack)
                return error.badRequest(10034, stack)
            new_user = mod.User(_userUsername, _userEmail, _userPseudo, _userPassword)
            mod.db.session.add(new_user)
            mod.db.session.commit()
            result = user_schema.dump(new_user).data
            return make_response(jsonify({'Message': 'OK', 'data': result}), 201)
        else:
            return error.badRequest(10001, "Veuillez remplir tous les champs obligatoire!")