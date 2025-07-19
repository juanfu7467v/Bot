from pyrogram import Client, filters
from pyrogram.types import Message
import os

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

app = Client(name="my_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# ID del bot a quien se envían los comandos, por ejemplo: @LEDER_BOT
DESTINO_BOT = "LEDER_BOT"  # sin @

@app.on_message(filters.private & filters.text)
async def handle_command(client: Client, message: Message):
    texto = message.text

    # Enviamos el mensaje al bot objetivo
    enviado = await client.send_message(chat_id=DESTINO_BOT, text=texto)

    # Esperamos su respuesta
    respuesta = await app.listen(DESTINO_BOT, timeout=20)

    # Reenviamos la respuesta al usuario
    await message.reply(respuesta.text)

if __name__ == "__main__":
    print("✅ Bot en funcionamiento...")
    app.run()
