import os
import requests
from flask import Flask, request, jsonify, send_file
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SARVAM_API_KEY")

app = Flask(__name__)

@app.route("/")
def home():
    return send_file("index.html")   # serves the web page

@app.route("/transcribe", methods=["POST"])
def transcribe():
    audio = request.files["audio"]   # the recording sent by the browser
    files = {"file": ("recording.wav", audio.read(), "audio/wav")}
    data = {"model": "saaras:v3", "language_code": "unknown"}
    headers = {"api-subscription-key": API_KEY}
    r = requests.post("https://api.sarvam.ai/speech-to-text",
                      headers=headers, files=files, data=data)
    return jsonify(r.json())

app.run(port=8000, debug=True)