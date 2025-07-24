from flask import Flask, request, jsonify
from pyrogram import Client
import os
import asyncio

# --- Configuración desde Variables de Entorno ---
# Estas son cruciales para la autenticación de tu bot de Telegram.
# ¡IMPORTANTE!: No compartas tu API_ID, API_HASH o SESSION_STRING públicamente.
# Para desarrollo, puedes poner valores directamente aquí, pero para producción
# DEBES usar variables de entorno para seguridad.
API_ID = int(os.environ.get("API_ID", "TU_API_ID_AQUI")) # Reemplaza con tu API ID real (de my.telegram.org)
API_HASH = os.environ.get("API_HASH", "TU_API_HASH_AQUI") # Reemplaza con tu API Hash real
SESSION_STRING = os.environ.get("SESSION_STRING", "") # Opcional: Tu cadena de sesión de Pyrogram si usas una sesión existente

# --- Configuración de la Aplicación Flask ---
app = Flask(__name__)

# Inicializa el cliente de Pyrogram de forma global.
# Se iniciará y detendrá mediante los "hooks" de ciclo de vida de Flask.
pyro_client = Client("bot_session", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# Bandera global para controlar si el cliente de Pyrogram ya se ha iniciado.
# Esto asegura que se inicie solo una vez.
pyro_client_started = False

# --- Hooks del Ciclo de Vida de Flask para el Cliente de Pyrogram ---

# NOTA IMPORTANTE: El decorador "@app.before_first_request" HA SIDO ELIMINADO EN FLASK 2.3+.
# EN SU LUGAR, usamos "@app.before_request" para iniciar el cliente de Pyrogram
# de forma condicional solo la primera vez que se recibe una solicitud.
@app.before_request
async def ensure_pyro_client_started():
    """
    Esta función se ejecuta antes de cada solicitud.
    Asegura que el cliente de Pyrogram se inicie solo una vez,
    la primera vez que se recibe una solicitud en la aplicación.
    """
    global pyro_client_started
    if not pyro_client_started:
        print("Intentando iniciar el cliente de Pyrogram...")
        try:
            await pyro_client.start()
            pyro_client_started = True
            print("Cliente de Pyrogram iniciado exitosamente.")
        except Exception as e:
            print(f"Error al iniciar el cliente de Pyrogram: {e}")
            # En un entorno de producción, deberías registrar este error
            # y posiblemente devolver una respuesta de error o deshabilitar la funcionalidad.

@app.teardown_appcontext
async def stop_pyro_client(exception=None):
    """
    Esta función se ejecuta cuando el contexto de la aplicación se cierra (ej. cuando el servidor se detiene).
    Asegura que el cliente de Pyrogram se detenga correctamente.
    """
    global pyro_client_started
    if pyro_client_started:
        print("Intentando detener el cliente de Pyrogram...")
        try:
            await pyro_client.stop()
            pyro_client_started = False
            print("Cliente de Pyrogram detenido exitosamente.")
        except Exception as e:
            print(f"Error al detener el cliente de Pyrogram: {e}")
            # Registra este error en un entorno de producción.

# --- Rutas de Flask ---

@app.route("/")
def home():
    """
    Una ruta simple para confirmar que la aplicación Flask está funcionando.
    """
    return "Bot funcionando correctamente."

@app.route("/enviar", methods=["POST"])
async def enviar():
    """
    Recibe una solicitud POST para enviar un mensaje a través de Pyrogram.
    Esta ruta ahora es asíncrona para poder usar operaciones 'await' de Pyrogram directamente.
    """
    data = request.get_json()
    chat_id = data.get("chat_id")
    mensaje = data.get("mensaje")

    # Valida los datos recibidos
    if not chat_id or not mensaje:
        return jsonify({"error": "chat_id y mensaje son requeridos"}), 400

    try:
        # Envía el mensaje usando el cliente de Pyrogram gestionado globalmente.
        # El cliente ya debería estar iniciado por el hook `before_request`.
        await pyro_client.send_message(chat_id, mensaje)
        return jsonify({"status": "Mensaje enviado con éxito"})
    except Exception as e:
        # Captura cualquier excepción durante el envío del mensaje (ej. chat_id no encontrado, problemas de red)
        print(f"Error al enviar mensaje: {e}")
        return jsonify({"error": f"Error al enviar mensaje: {e}"}), 500

# --- Punto de Entrada de la Aplicación ---
if __name__ == "__main__":
    # Cuando se ejecuta con `app.run()`, el servidor de desarrollo de Flask es síncrono.
    # Sin embargo, Flask 2.0+ soporta vistas asíncronas (`async def` en las rutas) y
    # funciones asíncronas para `before_request`/`teardown_appcontext`.
    # Para producción, normalmente usarías un servidor ASGI como Gunicorn con un worker Uvicorn
    # (ej. `gunicorn -w 4 -k uvicorn main:app`) para un mejor rendimiento asíncrono.
    app.run(host="0.0.0.0", port=3000, debug=True) # `debug=True` es útil para desarrollo
