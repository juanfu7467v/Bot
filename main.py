from flask import Flask, request, jsonify
from pyrogram import Client
import os

API_ID = int(os.environ.get("API_ID", "123456"))  # Reemplaza con tu API_ID
API_HASH = os.environ.get("API_HASH", "tu_api_hash")
SESSION_STRING = os.environ.get("SESSION_STRING", "tu_session_string")

app = Flask(__name__)
bot = Client("my_account", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

@app.route('/')
def index():
    return "Bot funcionando."

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    chat_id = data.get('chat_id')
    message = data.get('message')
    if not chat_id or not message:
        return jsonify({"error": "Faltan datos"}), 400

    async def enviar():
        async with bot:
            await bot.send_message(chat_id, message)

    import asyncio
    asyncio.run(enviar())

    return jsonify({"status": "Mensaje enviado con éxito"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
