import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from flask_jwt_extended import JWTManager

basedir = os.path.abspath(os.path.dirname(__file__))

# Create the Connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app

# Params to join the encodocker
DOCKER_NAME = 't_encoder'
DOCKER_PORT = 5001
DOCKER_FUNC = 'encoding'
DOCKER_ROUTE = "http://{}:{}/{}".format(DOCKER_NAME, DOCKER_PORT, DOCKER_FUNC)

# Configure the SQLAlchemy part of the app instance
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:pass@t_db/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = '/home/videos'
app.config['CORS_ENABLED'] = True

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)

jwt = JWTManager(app)