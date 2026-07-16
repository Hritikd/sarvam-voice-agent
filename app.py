import os
import base64
import requests
from flask import Flask, request, jsonify, send_file
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SARVAM_API_KEY")

app = Flask(__name__)

@app.route("/")
def home():
    return send_file("index.html")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    audio = request.files["audio"]
    files = {"file": ("recording.wav", audio.read(), "audio/wav")}
    data = {"model": "saaras:v3", "language_code": "unknown"}
    headers = {"api-subscription-key": API_KEY}
    r = requests.post("https://api.sarvam.ai/speech-to-text",
                      headers=headers, files=files, data=data)
    return jsonify(r.json())

@app.route("/speak", methods=["POST"])
def speak():
    body = request.get_json()          # read the text the page sent
    text = body["text"]
    language = body.get("language", "hi-IN")
    headers = {"api-subscription-key": API_KEY, "Content-Type": "application/json"}
    payload = {
        "inputs": [text],
        "target_language_code": language,
        "model": "bulbul:v2"
    }
    r = requests.post("https://api.sarvam.ai/text-to-speech",
                      headers=headers, json=payload)
    return jsonify(r.json())

app.run(port=8000, debug=True)