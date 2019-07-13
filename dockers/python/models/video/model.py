import sys, logging
from datetime import datetime
from flask import request, make_response, jsonify
import config 

logging.getLogger().setLevel(logging.INFO)

db = config.db
ma = config.ma

class Video(db.Model):
    __tablename__ = 'video'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45),  nullable=False)
    duration = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, nullable=False)
    source = db.Column(db.String(45), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    view = db.Column(db.Integer, nullable=False)
    enabled = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, name, duration, user_id, source, view, enabled):
        self.name = name
        self.duration = duration
        self.user_id = user_id
        self.source = source
        self.created_at = datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
        self.view = view
        self.enabled = enabled


class VideoSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'name', 'duration', 'user_id', 'source', 'created_at', 'view', 'enabled')


class VideoFormat(db.Model):
    __tablename__ = 'video_format'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(45),  nullable=False)
    uri = db.Column(db.String(45), nullable=False)
    video_id= db.Column(db.Integer, nullable=False)

    def __init__(self, code, uri, video_id):
        self.code = code
        self.uri = uri
        self.video_id = video_id



class VideoFormatSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'code', 'uri', 'video_id')