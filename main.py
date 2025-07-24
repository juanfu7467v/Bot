from flask import Flask
from pyrogram import Client
import os

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

app = Flask(__name__)

# Inicializamos Pyrogram Client
pyro_app = Client(
    name="anon",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

@app.before_first_request
def startup():
    pyro_app.start()

@app.route("/")
def home():
    return "Bot Pyrogram funcionando en Railway ✅"

@app.route("/me")
def get_me():
    user = pyro_app.get_me()
    return {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name
    }

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
