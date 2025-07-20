from flask import Flask, request, jsonify
from pyrogram import Client
import asyncio

# Configura tu sesión de Pyrogram (ya debes tenerla lista)
api_id = int("TU_API_ID")
api_hash = "TU_API_HASH"
session_string = "TU_SESSION_STRING"  # Copia la string generada por Pyrogram aquí

# Instancia el cliente de Pyrogram
app_client = Client(
    session_string=session_string,
    api_id=api_id,
    api_hash=api_hash
)

# Inicia Flask
app = Flask(__name__)

# Función para interactuar con @LEDER_BOT
async def enviar_comando_y_esperar_respuesta(comando):
    async with app_client:
        # Enviar el mensaje al bot
        mensaje = await app_client.send_message("LEDER_BOT", comando)

        # Esperar la respuesta (máx 10 segundos)
        for _ in range(20):
            await asyncio.sleep(0.5)
            respuestas = []
            async for r in app_client.get_chat_history("LEDER_BOT", limit=5):
                if r.reply_to_message and r.reply_to_message.message_id == mensaje.id:
                    respuestas.append(r)
            if respuestas:
                return respuestas[0].text  # Primera respuesta encontrada

        return "⛔ No se recibió respuesta del bot."

# Ruta GET para consultar
@app.route("/consulta", methods=["GET"])
def consulta():
    cmd = request.args.get("cmd")

    if not cmd:
        return jsonify({"error": "Parámetro 'cmd' requerido"}), 400

    # Ejecutar comando de forma asíncrona
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    resultado = loop.run_until_complete(enviar_comando_y_esperar_respuesta(cmd))

    return jsonify({"respuesta": resultado})

# Iniciar Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
