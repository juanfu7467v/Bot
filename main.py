from flask import Flask, request
from pyrogram import Client
import os
import asyncio

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")

XDATA_NUMERO = "51999999999"  # Cambia al número de XDATA si es necesario

app = Flask(__name__)

# Cliente Pyrogram global
app_client = Client(
    name="my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# Iniciamos el cliente de Pyrogram una sola vez
loop = asyncio.get_event_loop()
loop.run_until_complete(app_client.start())

@app.route("/")
def index():
    return "✅ Bot de envío de DNI activo."

@app.route("/dni", methods=["GET"])
def enviar_mensaje():
    dni = request.args.get("dni")
    if not dni:
        return {"error": "Parámetro 'dni' requerido"}, 400

    mensaje = f"/dni{dni}"

    try:
        loop.run_until_complete(app_client.send_message("me", f"🧪 Enviando mensaje a XDATA: {mensaje}"))
        loop.run_until_complete(app_client.send_message(XDATA_NUMERO, mensaje))
        return {"status": "Mensaje enviado correctamente"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
