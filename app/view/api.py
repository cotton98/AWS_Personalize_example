from flask import Blueprint, jsonify, json
import boto3
import pandas as pd

api = Blueprint("api", __name__)

personalize = boto3.client("personalize")
personalize_runtime = boto3.client("personalize-runtime")
iam = boto3.client("iam")
s3 = boto3.client("s3")
campaign_arn = "arn:aws:personalize:us-east-1:570872761770:campaign/recommend-campaignuser-epicmobile"

# 추천 id의 제목 매칭때문에 기존의 데이터를 불러옴
data = pd.read_csv(
    "./data/u.data", sep="\t", names=["USER_ID", "ITEM_ID", "RATING", "TIMESTAMP"]
)
data = data[data["RATING"] > 3.6]
data = data[["USER_ID", "ITEM_ID", "TIMESTAMP"]]

items = pd.read_csv("./data/u.item", sep="|", usecols=[0, 1], encoding="latin-1")
items.columns = ["ITEM_ID", "TITLE"]

#use_id는 1로 set, item_id는 기존 데이터에서 랜덤으로 뽑아서 설정
user_id, item_id, _ = data.sample().values[0]
user_id = 1
item_title = items.loc[items["ITEM_ID"] == item_id].values[0][-1]
#사전에 미리 정해진 user와 item의 id를 콘솔창에 출력함
print("USER: {}".format(user_id))
print("ITEM: {}".format(item_title))

# 연동이 잘 되는지 test용 request-response
get_recommendations_response = personalize_runtime.get_recommendations(
    campaignArn=campaign_arn, userId=str(user_id), itemId=str(item_id)
)

def get_movie_title(movie_id):
    movie_id = int(movie_id) - 1
    return items.loc[movie_id]["TITLE"]


def get_item_id(itemid):
    itemid = int(itemid) - 1
    return items.loc[itemid]["ITEM_ID"]


item_list = get_recommendations_response["itemList"]
title_list = []

for item in item_list:
    title = get_movie_title(item["itemId"])
    title_list.append(title)

# 사용자 id, 즉 1일때의 추천 item의 제목을 콘솔창에 출력
print("Recommendations: {}".format(json.dumps(title_list, indent=2)))


@api.route("/list/<userid>", methods=["GET"])
def get_load_list(userid):

    # 특정 카테고리 기반 추천, 추천데이터 필터 옵션도 넣을수 있는것으로 알고 있음
    get_recommendations_response = personalize_runtime.get_recommendations(
        campaignArn=campaign_arn, userId=str(userid), itemId=str(item_id)
    )

    user_item_list = get_recommendations_response["itemList"]
    user_itemid_list = []

    for item in user_item_list:
        item = get_item_id(item["itemId"])
        user_itemid_list.append(item)

    user_itemid_list = list([int(x) for x in user_itemid_list])

    return jsonify({"user_id": userid, "recommend_itemidlist": user_itemid_list})
