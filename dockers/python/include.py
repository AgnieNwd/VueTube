import secrets, logging
from itsdangerous import URLSafeSerializer
from datetime import datetime, timedelta
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required
                                , jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask_restful import reqparse

logging.getLogger().setLevel(logging.INFO)

import error
from models.users.model import User, UserSchema
from models.auth.model import Token, TokenSchema
from models.video.model import Video, VideoSchema, VideoFormat, VideoFormatSchema
from models.comment.model import Comment, CommentSchema
from models.users import user

import config
db = config.db
ma = config.ma

jwt_token = ""

######################## get #############################################
def get_username_by_id(user_id):
    name = User.query.get(user_id)
    if name is not None:
        data = UserSchema().dump(name).data
        return data['username']
    else:
        return error.badRequest(10001, "Impossible de récupérer l'username !")


def get_user_by_id(user_id):
    userbyid = User.query.get(user_id)
    if userbyid is None:
        return False
    data = UserSchema().dump(userbyid).data
    return data


def get_user_id_by_token(token):
    userId = Token.query.filter_by(code=token).first()
    if userId is not None:
        data = TokenSchema().dump(userId).data
        logging.info("INCLUDE MODULE :: PRINT DATA {} \n\n".format(data))
        return data['user_id']
    else:
        return False


def get_token_by_user(id_user):
    tok = Token.query.filter_by(user_id=id_user).first()
    if tok is not None:
        data = TokenSchema().dump(tok).data
        return data['code']
    else:
        return False


def get_user_id_by_video_id(video_id):
    id = Video.query.get(video_id)
    if id is not None:
        data = VideoSchema().dump(id).data
        return data['user_id']
    else:
        return False   



def get_format_by_video_id(video_id):
    video_format_schema = VideoFormatSchema(many=True)

    id = Video.query.get(video_id)
    if id is not None:
        all_format = VideoFormat.query.filter_by(video_id=video_id).all()
        data = video_format_schema.dump(all_format).data
        list = {}
        for row in data:
            list.update({row['code']: '1'})
        return list
    else:
        return False

"""
    Authentification
"""
def authen(usern, passwd):

    auth = User.query.filter_by(username=usern, password=passwd).first()
    if auth is not None:
        data = UserSchema().dump(auth).data
        return data['id']
    else:
        return 0


""" 
    TOKEN
"""
def add_token(token, id_user):
    new_token = Token(token, id_user)
    db.session.add(new_token)
    db.session.commit()


def delete_token(id_user):
    tok = Token.query.filter_by(user_id=id_user).first()
    db.session.delete(tok)
    db.session.commit()


def create_token():
    user_token = secrets.token_urlsafe()
    return user_token


"""
    JWT
"""
def create_JWT(username):
    user = User.query.filter_by(username=username).first()
    if user is not None:
        jwt_access_token = create_access_token(identity=username)
        jwt_refresh_token = create_refresh_token(identity=username)
        global jwt_token
        jwt_token = jwt_access_token
    else:
        jwt_token = ''


def get_jwt():
    global jwt_token

    return jwt_token


"""
    HEADER
"""

#prend le token dans le header
def header():
    header = reqparse.RequestParser()
    header.add_argument('Authorization', type=str, location="headers", help="unauthorized")
    head = header.parse_args()
    if head['Authorization'] == '':
        head['Authorization'] = None
    return head['Authorization']


"""
    DELETE
"""

#supp les infos utilisateur
def delete_all_by_user_id(id_user):
    vid = Video.query.filter_by(user_id=id_user).all()
    for i in range(len(vid)):
        data = VideoSchema(many=True).dump(vid).data
        dat = data[i]
        id = dat['id']
        delete_com_form_by_video_id(id)
    Video.query.filter_by(user_id=id_user).delete()
    Comment.query.filter_by(user_id=id_user).delete()
    db.session.commit()


#supp les infos video
def delete_com_form_by_video_id(id_video):
    Comment.query.filter_by(video_id=id_video).delete()
    VideoFormat.query.filter_by(video_id=id_video).delete()
    db.session.commit()


"""
    MAIL
"""
import requests
def send_email(type, email, username):
    create_JWT(username)

    jwt = get_jwt()
    your_data = {
        'type' : type,
        'email' : email
    }
    baerer = 'Bearer ' + jwt
    headers = {'Authorization': baerer}
    response = requests.get(url="http://t_mailer:5005/send", headers=headers, json=your_data)