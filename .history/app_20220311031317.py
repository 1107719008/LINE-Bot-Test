from unittest import result
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

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
    message = TextSendMessage(text="event.message.text")
    line_bot_api.reply_message(event.reply_token, message)

    



import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
