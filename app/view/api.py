import boto3
import json
import numpy as np
import pandas as pd
import time
from flask import Flask, Blueprint, jsonify, json, request

api = Blueprint('api',__name__)

#awspersonalize기본설정
personalize = boto3.client('personalize')
personalize_runtime = boto3.client('personalize-runtime')
iam = boto3.client("iam")
s3 = boto3.client("s3")
campaign_arn = "arn:aws:personalize:us-east-1:570872761770:campaign/recommend-campaignuser-epicmobile"
data = pd.read_csv('./data/u.data', sep='\t', names=['USER_ID', 'ITEM_ID', 'RATING', 'TIMESTAMP'])
data = data[data['RATING'] > 3.6]
data = data[['USER_ID', 'ITEM_ID', 'TIMESTAMP']]

#아이템 리스트 불러오기
items = pd.read_csv('./data/u.item', sep='|', usecols=[0,1], encoding='latin-1')
items.columns = ['ITEM_ID', 'TITLE']

user_id, item_id, _ = data.sample().values[0]
user_id = 1
item_title = items.loc[items['ITEM_ID'] == item_id].values[0][-1]
print("USER: {}".format(user_id))
print("ITEM: {}".format(item_title))

#추천리스트를 불러줄 켐페인 유저id, 아이템id등록
get_recommendations_response = personalize_runtime.get_recommendations(
    campaignArn = campaign_arn,
    userId = str(user_id),
    itemId = str(item_id)
)

def get_movie_title(movie_id) :
    movie_id = int(movie_id)-1
    return items.loc[movie_id]['TITLE']

item_list = get_recommendations_response['itemList']
#title_list = [items.loc[items['ITEM_ID'] == np.int(item['itemId'])].values[0][-1] for item in item_list] #3, 50, 432등 특정 숫자에서 오류나서 제외한 코드
title_list = []

for item in item_list :
    title = get_movie_title(item['itemId'])
    title_list.append(title)


print("Recommendations: {}".format(json.dumps(title_list, indent=2)))

@api.route('/list/<userid>', methods=['GET'])
def get_load_list(userid):
    if userid > '943' :
        return 'No user in service'

    get_recommendations_response = personalize_runtime.get_recommendations(
        campaignArn = campaign_arn,
        userId = str(userid),
        itemId = str(item_id)
    )

    user_item_list = get_recommendations_response['itemList']
    user_title_list = []

    for item in user_item_list :
        title = get_movie_title(item['itemId'])
        user_title_list.append(title)

    return jsonify({'user_id': userid, 'recommend_list' : user_title_list})