from flask import Flask, request
from pyrogram import Client
import os
import asyncio

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")
XDATA_NUMERO = "51999999999@c.us"  # Reemplaza con el número correcto si es necesario

app = Flask(__name__)

# Inicializa el cliente de Pyrogram
app_client = Client(
    name="my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# Arranca el cliente de Pyrogram
@app.before_request
def ensure_client_started():
    if not app_client.is_connected:
        asyncio.run(app_client.start())

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
        asyncio.run(app_client.send_message("me", f"🧪 Enviando mensaje a XDATA: {mensaje}"))
        asyncio.run(app_client.send_message("51999999999", mensaje))  # Puedes cambiar este número
        return {"status": "Mensaje enviado correctamente"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
