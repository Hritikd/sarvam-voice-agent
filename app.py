import os
import json
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

@app.route("/understand", methods=["POST"])
def understand():
    body = request.get_json()
    transcript = body["text"]

    system_prompt = (
        "You are a booking assistant. From the user's sentence, extract the "
        "action (book, cancel, or reschedule), the day, and the time. "
        "Reply with ONLY a JSON object and nothing else, in exactly this format: "
        '{"action": "...", "day": "...", "time": "..."}. '
        "Use 24-hour time like 18:00. If any field is missing, set it to \"unknown\"."
    )

    headers = {"api-subscription-key": API_KEY, "Content-Type": "application/json"}
    payload = {
        "model": "sarvam-105b",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": transcript}
        ]
    }
    r = requests.post("https://api.sarvam.ai/v1/chat/completions",
                      headers=headers, json=payload)

    # Pull the model's text out of the response
    try:
        raw = r.json()["choices"][0]["message"]["content"]
    except Exception:
        return jsonify({"error": "unexpected LLM response", "raw": r.json()})

    # The safety net: try to find and parse JSON, don't crash if it's messy
    intent = safe_parse_json(raw)
    if intent is None:
        return jsonify({"error": "could not parse intent", "raw": raw})

    return jsonify({"intent": intent, "raw": raw})

def safe_parse_json(text):
    """Try hard to extract a JSON object from a possibly-messy model reply."""
    try:
        return json.loads(text)          # clean case: it's pure JSON
    except Exception:
        pass
    # messy case: grab the substring between the first { and last }
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except Exception:
            return None
    return None

@app.route("/speak", methods=["POST"])
def speak():
    body = request.get_json()
    text = body["text"]
    language = body.get("language", "hi-IN")
    headers = {"api-subscription-key": API_KEY, "Content-Type": "application/json"}
    payload = {"inputs": [text], "target_language_code": language, "model": "bulbul:v2"}
    r = requests.post("https://api.sarvam.ai/text-to-speech",
                      headers=headers, json=payload)
    return jsonify(r.json())

@app.route("/translate", methods=["POST"])
def translate():
    body = request.get_json()
    text = body["text"]
    headers = {"api-subscription-key": API_KEY, "Content-Type": "application/json"}
    payload = {
        "input": text,
        "source_language_code": "auto",
        "target_language_code": body.get("target", "kn-IN"),
        "model": "mayura:v1"
    }
    r = requests.post("https://api.sarvam.ai/translate", headers=headers, json=payload)
    return jsonify(r.json())

app.run(port=8000, debug=True)