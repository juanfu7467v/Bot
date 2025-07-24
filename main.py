from flask import Flask
from pyrogram import Client
import os

app = Flask(__name__)

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

bot = Client(
    name="bot_session",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

@app.route('/')
def index():
    return 'Bot corriendo en Pyrogram + Flask con Railway'

@app.route('/enviar/<int:user_id>/<mensaje>')
def enviar_mensaje(user_id, mensaje):
    async def send():
        await bot.send_message(user_id, mensaje)
    bot.run(send())
    return f"Mensaje enviado a {user_id}: {mensaje}"

if __name__ == "__main__":
    bot.start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
