from flask import Flask, jsonify
from pyrogram import Client
import os

app = Flask(__name__)

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME", "my_session")

@app.route("/")
def index():
    return jsonify({
        "status": "ok",
        "message": "Bot funcionando correctamente."
    })

@app.route("/session")
def generate_session():
    try:
        with Client(session_name=SESSION_NAME, api_id=API_ID, api_hash=API_HASH) as app_client:
            string_session = app_client.export_session_string()
            return jsonify({
                "status": "success",
                "session_string": string_session
            })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
