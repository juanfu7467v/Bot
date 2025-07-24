from flask import Flask, request
from pyrogram import Client
import os
import asyncio

app = Flask(__name__)

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")

if not all([API_ID, API_HASH, SESSION_STRING]):
    raise Exception("Faltan variables de entorno: API_ID, API_HASH o SESSION_STRING")

client = Client(
    name="anon",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

@app.route("/")
def home():
    return "Bot de Pyrogram funcionando correctamente."

@app.route("/enviar", methods=["GET"])
def enviar_mensaje():
    numero = request.args.get("numero")
    mensaje = request.args.get("mensaje")

    if not numero or not mensaje:
        return "Faltan parámetros ?numero=...&mensaje=..."

    async def enviar():
        async with client:
            await client.send_message(numero, mensaje)

    asyncio.run(enviar())
    return f"Mensaje enviado a {numero}."

if __name__ == "__main__":
    app.run(debug=False, port=3000)
