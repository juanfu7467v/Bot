from flask import Flask, request, jsonify
from pyrogram import Client
import os

API_ID = int(os.environ.get("API_ID", "123456"))
API_HASH = os.environ.get("API_HASH", "your_api_hash")
SESSION_STRING = os.environ.get("SESSION_STRING", "")

app = Flask(__name__)
pyro_client = Client("bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

@app.route("/")
def home():
    return "Bot funcionando correctamente."

@app.route("/enviar", methods=["POST"])
def enviar():
    data = request.get_json()
    chat_id = data.get("chat_id")
    mensaje = data.get("mensaje")

    if not chat_id or not mensaje:
        return jsonify({"error": "chat_id y mensaje son requeridos"}), 400

    async def enviar_mensaje():
        async with pyro_client:
            await pyro_client.send_message(chat_id, mensaje)

    import asyncio
    asyncio.run(enviar_mensaje())
    return jsonify({"status": "Mensaje enviado con éxito"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
