from flask import Flask, jsonify
from pyrogram import Client
import os
import asyncio

app = Flask(__name__)

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

loop = asyncio.get_event_loop()
client = Client(name="bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

@app.route("/")
def home():
    return jsonify({"message": "Servidor Flask y Pyrogram funcionando correctamente."})

@app.route("/me")
def get_me():
    async def fetch_user():
        async with client:
            me = await client.get_me()
            return me.username or me.first_name

    username = loop.run_until_complete(fetch_user())
    return jsonify({"me": username})

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
