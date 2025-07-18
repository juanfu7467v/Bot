import asyncio
from flask import Flask, request, jsonify
from pyrogram import Client
import os

# Telegram bot objetivo
BOT_USERNAME = "LederData_bot"  # Cambia si tu bot es diferente

# Configuración Flask
app = Flask(__name__)

# Configuración Pyrogram
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session_string = os.environ.get("SESSION_STRING")

app_pyro = Client(name="anon", api_id=api_id, api_hash=api_hash, session_string=session_string)

@app.before_first_request
def start_pyrogram():
    loop = asyncio.get_event_loop()
    loop.create_task(app_pyro.start())

@app.route("/")
def index():
    return "✅ API para LederBot funcionando."

@app.route("/consulta", methods=["GET"])
async def consulta():
    dni = request.args.get("dni")
    tipo = request.args.get("tipo", "meta")  # meta por defecto

    comandos = {
        "meta": "/meta",
        "seeker": "/seeker",
        "afp": "/afp",
        "antpen": "/antpen",
        "antpol": "/antpol",
        "antjud": "/antjud",
        "con": "/con",
        "exd": "/exd",
        "tel": "/tel",
        "osiptel": "/osiptel"
    }

    comando = comandos.get(tipo.lower())
    if not comando:
        return jsonify({"error": "Tipo de comando no válido"}), 400

    mensaje = f"{comando} {dni}"
    try:
        await app_pyro.send_message(BOT_USERNAME, mensaje)
        await asyncio.sleep(3.5)
        mensajes = await app_pyro.get_chat_history(BOT_USERNAME, limit=1)
        respuesta = mensajes[0].text
        return jsonify({"respuesta": respuesta})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
