import sys, flask
from flask import Flask
from flask_cors import CORS
sys.path.insert(0, "./app/view")
import api

app = Flask(__name__)
cors = CORS(app)

app.register_blueprint(api.api, url_prefix="/recommend")

@app.route("/")
def hello_world():
    my_res = flask.Response("Hello world!")
    my_res.headers["Access-Control-Allow-Origin"] = "*"
    return my_res

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port="5000")
