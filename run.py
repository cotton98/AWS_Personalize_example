from flask import Flask, jsonify, request, Blueprint, json
from app.view import api

app = Flask(__name__)

app.register_blueprint(api.api, url_prefix='/recommend')

#기본 url
@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = '8080')