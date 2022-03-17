from unittest import result
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,PostbackAction,ButtonsTemplate

import json

from sqlalchemy import false
with open("Flask-LINE-Bot-Heroku/question.json") as f:
    q = json.load(f)


app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('gAc17pqOorE0IEwm6RW4KjU53I0eeodNvVvfyPZkw4Kepl8JFO+3b2nFp0h99vf8XCkdQDUs8ufsbkdEol6kg9n9nwkgzcai9n8DR33GIMXIn/1fUsFPB7C1xdLPsX9Q6izqQGaXKPPypLCtbePg+wdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('71678bf60ea8be36670b93441a29a737')

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
#0310
# 處理訊息
def Starting_Qusetion(q_num):
    buttons_template_message = TemplateSendMessage(
                    alt_text='Buttons template',
                    template=ButtonsTemplate(
                        thumbnail_image_url='https://example.com/image.jpg',
                        title='問題'+String(q_num+1),
                        text=q[q_num]['text'],
                        actions=[
                            PostbackAction(
                                label=q[q_num]['answer'][0]['label'],
                                display_text=q[q_num]['answer'][0]['label'],
                                data=q[q_num]['answer'][0]['data']
                            ),
                            PostbackAction(
                                label=q[q_num]['answer'][1]['label'],
                                display_text=q[q_num]['answer'][1]['label'],
                                data=q[q_num]['answer'][1]['data']
                            ),
                            PostbackAction(
                                label=q[q_num]['answer'][1]['label'],
                                display_text=q[q_num]['answer'][1]['label'],
                                data=q[q_num]['answer'][1]['data']
                            ),
                        ]
                    )
                )    
                



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text
    if get_message == '開始問答':
        Starting_Qusetion(count)

@handler.add(PostbackAction, message=PostbackAction)
def handle_postback(event):
    get_postback = event.postback.data
    if(get_postback == '答對'):
        try:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='恭喜答對！'))
            count+=1
            Starting_Qusetion(count)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

    else:
        try:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='答錯！'))
            Starting_Qusetion(count)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    if(count==2):
        try:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='獲得獎勵！'))
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))



import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
