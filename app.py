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


app = Flask(__name__)

line_bot_api = LineBotApi(
    'f1UkFaQj7dU1qoOdANntXBlmN/yd1+HssohiZXufOscLa7FAT9Wa3p2Tes92lb8s39/cG+htP/dyY2ApYYijsO7KwWb/Kh02yXn706pJstsmtTUtpuV0tYKtYXiR/XOIj9fC+VYKmIvOA8T4rctmTwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('3c0582d8762771c056e4339a3c759ce5')


@app.route("/")
def home():
    return 'Test is OK'

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
    if 'hi' in event.message.text:
        line_bot_api.reply_message(
            event.reply_token,  # 回覆後即丟棄此token
            TextSendMessage(text='今天天氣真好'))


'''
    line_bot_api.reply_message(
        event.reply_token,  # 回覆後即丟棄此token
        TextSendMessage(text=event.message.text))
'''

if __name__ == "__main__":
    app.run()
