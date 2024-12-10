# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('fYrQ6RGmKwv7r4gnXfs56R4K3/tDydj51WnAdRo9T/sTOaIav/+uj3AYzv9IebRq0/sB104GUAfq+C+kphARlt14JG5NX++jYYYpUVcmNNPQwxW6G4B7/UxiDsw778WutAuTHbC+uU1HPysUPA45nQdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('086911a76d0adbc5b6c921919254aacc')

line_bot_api.push_message('Ub7e1509c5ddac28513c42acf588b18df', TextSendMessage(text='你可以開始了'))

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
        abort(400)

    return 'OK'

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if re.match('告訴我秘密',message):
        confirm_template_message = TemplateSendMessage(
            alt_text='這是TemplateSendMessage',
            template=ConfirmTemplate(
                text='你喜歡韓國嗎？',
                actions=[
                    PostbackAction(
                        label='喜歡',
                        display_text='超喜歡',
                        data='action=其實不喜歡'
                    ),
                    MessageAction(
                        label='讚',
                        text='讚讚'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, confirm_template_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
