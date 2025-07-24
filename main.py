from flask import Flask, request, jsonify
from pyrogram import Client
import os

# Reemplaza con tu Session String de usuario
SESSION_STRING = os.environ.get("SESSION_STRING")  # Puedes definirlo en variables de entorno

API_ID = int(os.environ.get("API_ID", "123456"))  # Coloca aquí tu API_ID de my.telegram.org
API_HASH = os.environ.get("API_HASH", "tu_api_hash")  # Coloca tu API_HASH

app = Flask(__name__)

# Crea el cliente de Pyrogram
pyro_client = Client(
    name="my_session",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# Inicia el cliente antes de la primera solicitud
@app.before_request
def start_pyrogram():
    if not pyro_client.is_connected:
        pyro_client.connect()

@app.route("/")
def home():
    return "Servidor funcionando correctamente."

@app.route("/enviar", methods=["GET"])
def enviar_mensaje():
    try:
        chat_id = request.args.get("chat_id")
        mensaje = request.args.get("mensaje")
        if not chat_id or not mensaje:
            return jsonify({"error": "chat_id y mensaje son requeridos"}), 400

        pyro_client.send_message(chat_id, mensaje)
        return jsonify({"status": "mensaje enviado"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
