from flask import Flask, Blueprint, request, jsonify, json
from view.personalize import returnlist, returnuserid

api = Blueprint('api',__name__)

@api.route('/get', methods=['GET'])
def get_load_list():
    list = returnlist()
    return jsonify(list)

@api.rout('/get/<userid>', methods=['GET'])
def get_uesrid(userid):
    return userid