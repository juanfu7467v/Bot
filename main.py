from flask import Flask
from pyrogram import Client
import os

app = Flask(__name__)

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

bot = Client(name="my_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

@app.route('/')
def home():
    return "Bot funcionando correctamente en Railway ✅"

@app.before_first_request
def start_bot():
    bot.start()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
