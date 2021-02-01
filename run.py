from flask import Flask, jsonify, request, Blueprint, json
import sys
sys.path.insert(0, './app/view')
import api

app = Flask(__name__)

app.register_blueprint(api.api, url_prefix='/recommend')

#기본 url
@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=False, host = '0.0.0.0', port = '5000')