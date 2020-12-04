from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import requests
import json

#from get_weather import get_weathers

app = Flask(__name__)

line_bot_api = LineBotApi(
    'f1UkFaQj7dU1qoOdANntXBlmN/yd1+HssohiZXufOscLa7FAT9Wa3p2Tes92lb8s39/cG+htP/dyY2ApYYijsO7KwWb/Kh02yXn706pJstsmtTUtpuV0tYKtYXiR/XOIj9fC+VYKmIvOA8T4rctmTwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('3c0582d8762771c056e4339a3c759ce5')


@app.route("/")
def home():
    return 'Test OK'

# 監聽所有來自 /callback 的 Post Request


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    file = requests.get(
        "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization=CWB-C7DBCECE-6033-49AA-8A2F-B713168055B4&downloadType=WEB&format=JSON")
    file_json = file.json()
    location = file_json['cwbopendata']['dataset']['location']

    taiwan_city_dict = {'台北市': 0, '新北市': 1, '桃園市': 2, '台中市': 3, '台南市': 4, '高雄市': 5, '基隆市': 6, '新竹縣': 7, '新竹市': 8, '苗栗縣': 9,
                        '彰化縣': 10, '南投縣': 11, '雲林縣': 12, '嘉義縣': 13, '嘉義市': 14, '屏東縣': 15, '宜蘭縣': 16, '花蓮縣': 17, '台東縣': 18,
                        '澎湖縣': 19, '金門縣': 20, '連江縣': 21}  # 縣市編碼

    request_message = str(event.message.text)
    loc_name = 0  # 預設為台北市
    predict = False  # 預設不做預報
    location_name = request_message[0:3]  # 讀取使用者訊息前三個字判斷位置

    if location_name in taiwan_city_dict:
        loc_name = taiwan_city_dict[location_name]  # str(縣市) to int(縣市)
    if '預報' in request_message:  # 若使用者訊息包含預報
        predict = True

    Tmax = location[loc_name]['weatherElement'][1]['time']
    Tmin = location[loc_name]['weatherElement'][2]['time']
    feel = location[loc_name]['weatherElement'][3]['time']
    pop = location[loc_name]['weatherElement'][4]['time']

    """weather = '{}溫度: {}~ {}度, 降雨機率: {}%, 天氣: {}'.format(location[loc_name]['locationName'], Tmax[0]['parameter']['parameterName'],
                                                        Tmin[0]['parameter']['parameterName'], pop[0]['parameter']['parameterName'], feel[0]['parameter']['parameterName'])"""
    weather = ''
    if True:
        if predict:
            period = 3
        else:
            period = 1
        for i in range(period):
            time_start = Tmax[i]['startTime'][0:10] + \
                ' ' + Tmax[i]['startTime'][11:16]
            time_end = Tmax[i]['endTime'][11:16]
            weather_each_time = '{}~{}, {}溫度: {}~ {}度, 降雨機率: {}%, 天氣: {}'.format(time_start, time_end, location[loc_name]['locationName'], Tmax[i]['parameter'][
                                                                                 'parameterName'], Tmin[i]['parameter']['parameterName'], pop[i]['parameter']['parameterName'], feel[i]['parameter']['parameterName']) + '\n'
            weather += weather_each_time
    reply = weather

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply))


if __name__ == "__main__":
    app.run()
