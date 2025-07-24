from flask import Flask, request, jsonify
from pyrogram import Client
from pyrogram.types import Message
import asyncio
import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")

app = Flask(__name__)

bot = Client(
    name="my_account",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

@app.before_request
def ensure_client_started():
    if not bot.is_connected:
        asyncio.run(bot.start())

@app.route("/")
def home():
    return "✅ Bot Pyrogram activo."

@app.route("/consulta", methods=["GET"])
def consultar_dni():
    dni = request.args.get("dni")
    if not dni:
        return jsonify({"error": "Parámetro 'dni' es requerido"}), 400

    mensaje = f"/dni{dni}"

    async def enviar_y_esperar():
        # Enviar el mensaje al bot
        await bot.send_message("@LederDataBot", mensaje)

        # Esperar la respuesta del bot
        async for response in bot.listen("@LederDataBot", timeout=10):
            if isinstance(response, Message) and response.text:
                return response.text

        return None

    try:
        resultado = asyncio.run(enviar_y_esperar())

        if resultado:
            return jsonify({"respuesta": resultado}), 200
        else:
            return jsonify({"error": "No se recibió respuesta del bot."}), 504

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
