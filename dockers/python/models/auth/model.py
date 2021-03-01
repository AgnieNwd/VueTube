import logging
from datetime import datetime, timedelta
from config import db, ma

class Token(db.Model):
    __tablename__ = 'token'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(120), unique=True, nullable=True)
    expired_at = db.Column(db.DateTime, unique=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def __init__(self, code, user_id):
        self.code = code
        self.expired_at = datetime.now()+ timedelta(hours=4)
        self.user_id = user_id


class TokenSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('code', 'user_id', 'expired_at')
        