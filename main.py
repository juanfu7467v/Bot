from pyrogram import Client, filters
from pyrogram.enums import ChatType
from flask import Flask, request, jsonify
import asyncio
import os

# Variables de entorno
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

# Usuario objetivo
BOT_USERNAME = "LEDER_BOT"

# Crear cliente de Pyrogram
app_pyrogram = Client(name="my_session", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# Crear servidor Flask
app = Flask(__name__)

# Variable para almacenar respuestas
pending_responses = {}

@app.route("/consulta", methods=["GET"])
def consulta():
    comando = request.args.get("comando")
    valor = request.args.get("valor")

    if not comando or not valor:
        return jsonify({"error": "Parámetros requeridos: comando y valor"}), 400

    mensaje = f"/{comando} {valor}"
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response = loop.run_until_complete(enviar_comando_y_esperar_respuesta(mensaje))
    return jsonify({"respuesta": response})


async def enviar_comando_y_esperar_respuesta(mensaje):
    async with app_pyrogram:
        chat = await app_pyrogram.get_chat(BOT_USERNAME)
        sent = await app_pyrogram.send_message(chat.id, mensaje)

        # Esperamos respuesta del bot
        for _ in range(20):  # Máximo 20 intentos (aprox 20 segundos)
            await asyncio.sleep(1)
            async for msg in app_pyrogram.get_chat_history(chat.id, limit=5):
                if msg.reply_to_message and msg.reply_to_message.id == sent.id:
                    return msg.text
        return "❌ No se recibió respuesta del bot."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
