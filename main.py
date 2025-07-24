from flask import Flask, request, jsonify
from pyrogram import Client
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
import threading
import asyncio
import time

api_id = 123456  # ← Reemplaza con tu API_ID
api_hash = "tu_api_hash"  # ← Reemplaza con tu API_HASH
session_name = "mi_sesion"  # nombre de sesión (archivo generado)

app = Flask(__name__)
loop = asyncio.get_event_loop()
app_messages = []

# Inicializar Pyrogram
client = Client(session_name, api_id=api_id, api_hash=api_hash)

# Guardar la última respuesta de @LederDataBot
respuesta_dni = {}

@app.route("/")
def home():
    return "Servidor Pyrogram activo."

@app.route("/consulta")
def consulta_dni():
    dni = request.args.get("dni")
    if not dni or len(dni) != 8:
        return jsonify({"error": "DNI inválido"}), 400

    mensaje = f"/dni{dni}"
    try:
        respuesta_dni.pop(dni, None)  # Limpiar respuesta anterior si existe
        client.send_message("LederDataBot", mensaje)
    except Exception as e:
        return jsonify({"error": f"Error al enviar mensaje: {e}"}), 500

    # Esperar respuesta (máx 10 segundos)
    for _ in range(20):
        if dni in respuesta_dni:
            return jsonify({"dni": dni, "respuesta": respuesta_dni[dni]})
        time.sleep(0.5)

    return jsonify({"error": "Sin respuesta del bot"}), 504


def recibir_mensajes(client: Client, message: Message):
    if message.from_user and message.from_user.username == "LederDataBot":
        texto = message.text
        if texto and texto.startswith("DNI:"):
            dni_enviado = texto.split("DNI:")[1].split("\n")[0].strip()
            respuesta_dni[dni_enviado] = texto


def iniciar_pyrogram():
    client.add_handler(MessageHandler(recibir_mensajes))
    client.run()


if __name__ == "__main__":
    threading.Thread(target=iniciar_pyrogram, daemon=True).start()
    app.run(host="0.0.0.0", port=3000)
