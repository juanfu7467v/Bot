from flask import Flask, request, jsonify
from pyrogram import Client
import os
import asyncio

# Crear app Flask
app = Flask(__name__)

# Variables de entorno desde Railway
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

# Inicializar cliente de Pyrogram
client = Client("my_session", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# Iniciar cliente de Pyrogram al arrancar el servidor
loop = asyncio.get_event_loop()
loop.run_until_complete(client.start())

@app.route("/")
def index():
    return "✅ Bot activo con Pyrogram"

@app.route("/dni", methods=["GET"])
def buscar_dni():
    dni = request.args.get("dni")
    if not dni:
        return jsonify({"error": "Falta el parámetro 'dni'"}), 400

    try:
        mensaje = f"/dni{dni}"
        numero_bot = "51999999999@c.us"  # Reemplaza con el número correcto del bot
        loop.run_until_complete(client.send_message(numero_bot, mensaje))
        return jsonify({"status": "Mensaje enviado correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
