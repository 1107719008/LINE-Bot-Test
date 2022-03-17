from unittest import result
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,PostbackAction,ButtonsTemplate


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
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #message = TextSendMessage(text="hi")
    #line_bot_api.reply_message(event.reply_token, message)

    get_message = event.message.text
    
    if get_message == '開始問答':
        try:
            buttons_template_message = TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://example.com/image.jpg',
                    title='問題一',
                    text='請問數位系總共有幾個攤位',
                    actions=[
                        PostbackAction(
                            label='5',
                            display_text='5',
                            data='答錯'
                        ),
                        PostbackAction(
                            label='11',
                            display_text='11',
                            data='答錯'
                        ),
                        PostbackAction(
                            label='13',
                            display_text='13',
                            data='答對'
                        ),
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token,buttons_template_message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))



import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
