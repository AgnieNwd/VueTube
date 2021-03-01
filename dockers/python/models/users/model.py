import logging
from datetime import datetime
import config

logging.getLogger().setLevel(logging.INFO)

db = config.db
ma = config.ma


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pseudo = db.Column(db.String(120), nullable=True)
    password = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.String(120), nullable=False)
    
    def __init__(self, username, email, pseudo, password):
        self.username = username
        self.email = email
        self.pseudo = pseudo
        self.password = password
        self.created_at = datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


class UserSchema(ma.ModelSchema):
    class Meta:
        fields = ('id', 'username', 'email', 'pseudo', 'created_at')
        model = User
        sqla_session = db.session
