from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

# 環境変数から LINE Bot の設定を取得
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("QyqwdM5mHrHNXLiPU1Iuu0Woixo0D5fjgmrumhZ2+mwW1u/zG0IRvTK1cRR11ytHnHS6LOpoZkP5qPFdlsCOcx6AeRck1EpgXyOazyJJc75Q3XJCGMqdo5d+DZn9phKPEl9ycumoFqrHAe0FBA+lWwdB04t89/1O/w1cDnyilFU=")
LINE_CHANNEL_SECRET = os.getenv("21a1e8bf74ff783af8aff153ad5a1dfb")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/", methods=["GET"])
def home():
    return "LINE Bot is running!"

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    reply_message = f"あなたのメッセージ: {user_message}"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
