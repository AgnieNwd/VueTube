import os
import connexion
#from flask_jwt_extended import JWTManager

basedir = os.path.abspath(os.path.dirname(__file__))

# Create the Connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app

# Configure the SQLAlchemy part of the app instance
#app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
#app.config['UPLOAD_FOLDER'] = '/home/videos'
#app.config['CORS_ENABLED'] = True

#jwt = JWTManager(app)