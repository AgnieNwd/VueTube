from flask import make_response
from flask_jsonpify import jsonify
from datetime import datetime, timedelta
import re
import logging

from models.users.model import User, UserSchema
from models.video.model import Video, VideoSchema
from models.comment.model import Comment, CommentSchema
from models.auth.model import Token, TokenSchema

import include
#from SchemaSQLA import Token, TokenSchema, User, UserSchema, Video, VideoSchema
"""
Return number of ints in user_id
"""

def ifId_video(id_video):
    if ifIsNum(id_video) is False:
        return False
    vid = Video.query.get(id_video)
    if vid is not None:
        data = VideoSchema().dump(vid).data
        return data['id']
    else:
        return False


def ifId_comment(id_com):
    if ifIsNum(id_com) is False:
        return False
    com = Comment.query.get(id_com)
    if com is not None:
        data = CommentSchema().dump(com).data
        return data['id']
    else:
        return False


def badRequest(code, message_data):
    return make_response(jsonify({"Message": "Bad Request", "code": code, "data": [message_data]}), 400)


def unauthorized():
    return make_response(jsonify({"Message": "Unauthorized"}), 401)

def notFound():
    return make_response(jsonify({"Message": "Not found"}), 404)


def forbidden():
    return make_response(jsonify({"Message": "Forbidden"}), 403)


def tchek_password(passwd):
    if len(passwd) < 8:
        return " Mot de passe trop court, "
    else:
        return ""


def ifId(id_user):
    if ifIsNum(id_user) is False:
        return False
    id = User.query.get(id_user)
    if id is not None:
        result = UserSchema().dump(id).data
        return result['id']
    else:
        return False


def tchek_username(user):
    usern = User.query.filter_by(username=user).first()
    if usern is not None:
        return "Cette username est déjà utilisé, "
    else:
        return ""


def tchek_email(mail):
    match = re.match('^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', mail)
    if match == None:
        return 'Mail invalide, '

    Email = User.query.filter_by(email=mail).first()
    if Email is not None:
        return "Cette email est déjà utilisée, "
    else:
        return ""


def tchek_form_put_user(_userPassword, _userEmail, _userUsername, dataUser, dataEmail):
    stack = ""
    if _userPassword != "":
        stack = str(tchek_password(_userPassword))
    if dataUser != _userUsername and _userUsername != "":
        stack = stack + str(tchek_username(_userUsername))
    if dataEmail != _userEmail and _userEmail != "":
        stack = stack + str(tchek_email(_userEmail))
    return stack


def ifToken(token_data):
    token = False
    tok = Token.query.filter_by(code=token_data).first()

    if tok is not None:
        data = TokenSchema().dump(tok).data
        #if data['code'] == token_data:
        token = True
    return token


def ifIsNum(id):
    number =  ["0","1","2","3","4","5","6","7","8","9"]
    leng = len(id)
    lengn = len(number)
    isInt = 0
    for i in range(leng):
        for n in range(lengn):
            if id[i] == number[n]:
                isInt = isInt + 1
    if isInt == leng:
        return True
    return False


def tchek_token_expiration(id_user):
    expir = Token.query.filter_by(user_id=id_user).first()
    if expir is not None:
        data = TokenSchema().dump(expir).data
        if data['expired_at'] < datetime.now().strftime("%Y-%m-%d %H:%M:%S"):
            include.delete_token(id_user)
            return True
        else:
            return False
    else:
        return True

def isBool(v):
    logging.info("PRINT V : {} \n\n".format(v))
    if v in ('yes', 'true', 't', 'y', '1', 1):
        return True
    elif v in ('no', 'false', 'f', 'n', '0', 0):
        return False
    else:
        return 'Boolean Value Expected.'
        raise argparse.ArgumentTypeError('Boolean value expected.')