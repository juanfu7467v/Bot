from flask import Flask
from pyrogram import Client
import asyncio
import os

app = Flask(__name__)

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

bot = Client(
    name="my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# Función para iniciar el bot en segundo plano
def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bot.start())
    print("✅ Bot de Pyrogram iniciado")

# Iniciar el bot cuando Flask arranca
@app.before_serving
async def startup():
    asyncio.create_task(bot.start())

@app.route('/')
def home():
    return "✅ Bot corriendo en Railway"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
