import pymysql.cursors
import requests
import error
import user
from itsdangerous import URLSafeSerializer
from datetime import datetime, timedelta
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required
                                , jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

# conn to db
def db_connect():
    return pymysql.connect(host='t_db',
                           user='user',
                           password='pass',
                           db='mydb',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)


db = db_connect()
jwt_token = ""


######################## get #############################################
def get_username_by_id(user_id):
    with db.cursor() as authenti:
        query = "SELECT username from user where id = {}".format(user_id)
        if authenti.execute(query) == 1:
            return authenti.fetchone()
        else:
            return error.ifIsNone(10001, "Impossible de récupérer l'username !")


def get_user_by_id(user_id):
    with db.cursor() as cursor:
        id = error.ifIsInt(user_id)
        #Pour gérer si l'user est bien le proprio de la ressource mais problématique
        query = "SELECT id, username, created_at, pseudo FROM user WHERE id= '{}'".format(user_id)
        if user.get_id_user() == user_id:
            query = "SELECT id, username, created_at, email, pseudo FROM user WHERE id= '{}'".format(user_id)
        if id == len(user_id) and cursor.execute(query) == 1:
            return cursor.fetchall()
        else:
            return False


############ Authentification ########################
def authen(usern, passwd):
    with db.cursor() as cursor:
        query = "SELECT id FROM user WHERE username = '{}' and password = '{}'".format(usern, passwd)
        if cursor.execute(query) == 1:
            idkey = cursor.fetchone()
            id = idkey['id']
            return id
        else:
            return 0


############ token ###############
def add_token(token, expire, id_user):
    with db.cursor() as cursor:
        query = "INSERT INTO token (code, expired_at, user_id) VALUES ('{}', '{}', '{}')".format(token, expire, id_user)
        if cursor.execute(query):
            db.commit()


def delete_token(id_user):
    with db.cursor() as cursor:
        query = "DELETE FROM token where user_id ='{}'".format(id_user)
        if cursor.execute(query):
            db.commit()


def create_token():
    basic_token = URLSafeSerializer('secret-key')
    user_token = basic_token.dumps([1, 2, 3, 4, 5])
    return user_token


def token_expiration():
    return datetime.now() + timedelta(hours=4)


def tchek_token_expiration(id_user):
    with db.cursor() as cursor:
        query = "SELECT expired_at FROM token where user_id = {}".format(id_user)
        if cursor.execute(query) == 1:
            data = cursor.fetchone()
            expired_at = data['expired_at']
            if expired_at < datetime.now():
                delete_token(id_user)
                return True
            else:
                return False
        else:
            return True


def get_token_by_user(id_user):
    with db.cursor() as cursor:
        query = "SELECT code FROM token where user_id = {}".format(id_user)
        if cursor.execute(query) == 1:
            data = cursor.fetchone()
            return data
        else:
            return False


def ifToken(id_user):
    with db.cursor() as cursor:
        query = "SELECT user_id FROM token where user_id = {}".format(id_user)
        if cursor.execute(query) == 1:
            return True
        else:
            return False

######## jwt ##########################
def create_JWT(username):
    jwt_access_token = create_access_token(identity=username)
    jwt_refresh_token = create_refresh_token(identity=username)
    global jwt_token
    jwt_token = jwt_access_token


def get_jwt():
    global jwt_token
    return jwt_token