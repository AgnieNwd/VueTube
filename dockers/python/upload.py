import os
import logging
from flask import Flask, flash, request, redirect, url_for, make_response, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_jsonpify import jsonify
from flask_restful import Resource
import config

ALLOWED_EXTENSIONS = set(['webm', 'mkv', 'flv', 'avi', 'mpg','mpeg', 'mov', 'wmv', 'mp4', 'm4p'])


class Upload(Resource):
    def allowed_file(self, file_name):
        return '.' in file_name and file_name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def upload_file(self):
        logging.info("Uploading in progress …\n")
        if request.method == 'POST':
            if 'source' not in request.files:
                return "no file"
            file = request.files['source']
            if file.filename == '':
                return "no filename"
            if file and self.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                if not os.path.exists(config.app.config['UPLOAD_FOLDER']):
                    os.mkdir(config.app.config['UPLOAD_FOLDER'])
                file.save(os.path.join(config.app.config['UPLOAD_FOLDER'], filename))
                filePath = config.app.config['UPLOAD_FOLDER'] + '/' + filename
                return filePath
                #return redirect(url_for('uploaded_file', filename=filename))
            else:
                return make_response(jsonify({'Message':'something went wrong'}))
            return make_response("ok")

    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'],filename)
