from flask import Flask, request
from pyrogram import Client
import asyncio
import os

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session_string = os.environ.get("SESSION_STRING")  # Generado previamente con pyrogram

app = Flask(__name__)

bot = Client("my_account", api_id=api_id, api_hash=api_hash, session_string=session_string)

@app.route("/consulta", methods=["GET"])
def consulta():
    dni = request.args.get("dni")
    if not dni or not dni.isdigit() or len(dni) != 8:
        return {"status": "error", "message": "DNI inválido"}, 400

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(enviar_y_esperar(dni))
    return result

async def enviar_y_esperar(dni):
    numero_bot = "LederDataBot"
    mensaje = f"/dni{dni}"

    async with bot:
        enviado = await bot.send_message(numero_bot, mensaje)
        await asyncio.sleep(5)  # Espera por la respuesta (ajustable)

        respuestas = []
        async for msg in bot.get_chat_history(numero_bot, limit=5):
            if msg.reply_to_message and msg.reply_to_message.id == enviado.id:
                respuestas.append(msg.text)

        if respuestas:
            return {"status": "ok", "data": respuestas[0]}
        else:
            return {"status": "error", "message": "No se recibió respuesta"}

# Inicia el cliente fuera del decorador
if __name__ == "__main__":
    bot.start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
