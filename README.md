# Sarvam Voice Agent 🎙️

A multilingual voice-based appointment booking agent built entirely on Sarvam AI's stack. Speak naturally in Hindi (or code-mixed Hinglish) and the agent understands your intent, checks availability, negotiates an alternative if your slot is taken, and confirms the booking — all in voice.

**🔗 Live demo:** https://sarvam-voice-agent-xsc1.onrender.com
(Free tier — first load may take ~50s while the server wakes up.)

---

## What it does

Speak: "Mujhe Tuesday shaam 6 baje appointment book karna hai."

The agent:
1. **Transcribes** your speech (Saaras STT)
2. **Understands** intent — extracts action, day, and time as structured data (Sarvam-105B)
3. **Acts** — checks a calendar, and if the slot is taken, offers the next available one
4. **Responds** in natural Hindi voice (Bulbul TTS)
5. **Remembers** the conversation — say "Haan" and it books the offered slot

This is the core perceive → understand → act → respond loop that production voice agents run at scale.

---

## Architecture

Browser (mic) → audio → Flask server → Browser (plays response)

Inside the Flask server:
- **Saaras v3** → speech to text
- **Sarvam-105B** → intent extraction (returns structured JSON)
- **booking logic** → slot check + alternative + per-session memory
- **Bulbul v2** → text to speech

**Session memory:** conversation state is held per-session so multi-turn exchanges (offer → confirm) work correctly across separate voice inputs.

---

## Tech stack

- **Sarvam AI APIs:** Saaras (STT), Sarvam-105B (LLM), Bulbul (TTS)
- **Backend:** Python, Flask, Gunicorn
- **Frontend:** vanilla JS (MediaRecorder API)
- **Deployment:** Render

---

## Run locally

git clone https://github.com/Hritikd/sarvam-voice-agent.git
cd sarvam-voice-agent
pip install -r requirements.txt
echo "SARVAM_API_KEY=your_key_here" > .env
python app.py

Open http://127.0.0.1:8000

---

## Engineering notes

A few things surfaced while building that are worth knowing for anyone working on Indic voice agents:

- **ASR self-correction handling:** when a speaker fumbles ("kal — I mean Tuesday"), the transcriber keeps both fragments, and downstream intent extraction can mis-combine them. Real deployments need disfluency handling upstream of the LLM.
- **Time-of-day inference:** Saaras occasionally drops qualifiers like "shaam" (evening), leaving the LLM to infer AM vs PM. Sarvam-105B recovers this reasonably — but non-deterministically — which matters when a booking outcome depends on it.
- **Single-word confirmations are fragile:** short utterances like "haan" have no surrounding context for the ASR to anchor on and get garbled easily. Production agents lean on readbacks or tap-to-confirm rather than open "say yes."
- **Graceful degradation:** the pipeline is defensive — a failed or throttled model call returns a clear fallback rather than crashing the agent.

---

## Built by

Hritik Datta (https://github.com/Hritikd) — exploring what it takes to build real multilingual voice agents on India's sovereign AI stack.
