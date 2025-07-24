from flask import Flask
from pyrogram import Client
import os

api_id = int(os.environ.get("API_ID", "123456"))  # cambia por tus datos reales
api_hash = os.environ.get("API_HASH", "tu_api_hash")
session_string = os.environ.get("SESSION_STRING", None)

app = Flask(__name__)
bot = Client(name="bot", api_id=api_id, api_hash=api_hash, session_string=session_string)

@app.route("/")
def home():
    return "✅ Bot activo."

@app.before_first_request
def start_bot():
    bot.start()
    print("🤖 Bot iniciado.")

@app.route("/stop")
def stop_bot():
    bot.stop()
    return "❌ Bot detenido."

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
