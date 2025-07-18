import os
from flask import Flask
from pyrogram import Client
import logging

# Activa el logging para debug
logging.basicConfig(level=logging.INFO)

# Cargar variables de entorno
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session_string = os.environ.get("SESSION_STRING")

# Inicializar bot de Pyrogram
app_pyrogram = Client(
    name="my_bot",
    api_id=api_id,
    api_hash=api_hash,
    session_string=session_string
)

# Inicializar Flask
app = Flask(__name__)

@app.before_first_request
def start_bot():
    print("Iniciando bot de Pyrogram...")
    app_pyrogram.start()
    print("✅ Bot iniciado exitosamente.")

@app.route("/")
def home():
    return "Bot de Telegram está corriendo en Flask con Pyrogram ✅"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
