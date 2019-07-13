import sys, logging
from datetime import datetime
from flask import request, make_response, jsonify
import config 

logging.getLogger().setLevel(logging.INFO)

db = config.db
ma = config.ma

class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.String(256),  nullable=True)
    user_id = db.Column(db.Integer, nullable=False)
    video_id = db.Column(db.Integer, nullable=False)

    def __init__(self, body, user_id, video_id):
        self.body = body
        self.video_id = video_id
        self.user_id = user_id


class CommentSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'body', 'user_id', 'video_id')