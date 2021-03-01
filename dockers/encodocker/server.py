import logging
from flask import Flask
from flask_restful import Resource, Api
import config
import encoding
from flask_jsonpify import jsonify
import receive

app = config.app

apencode = Api(app)

encoder = encoding.Encoding()

apencode.add_resource(encoding.Encoding, '/encoding', methods=['GET', 'POST'])

logging.getLogger().setLevel(logging.INFO)

def listen():
    # Build & Start to listening the rabbit MQ queue
    listener = receive.Consumer()
    listener.start()

if __name__ == '__main__':
    logging.info("Rabbit MQ is listening…")
    listen()
    app.run(host='0.0.0.0', port=5001, debug=True)