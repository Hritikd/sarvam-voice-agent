# Sarvam Voice Agent 🎙️

A multilingual voice-based appointment booking agent built entirely on [Sarvam AI](https://www.sarvam.ai)'s stack. Speak naturally in Hindi (or code-mixed Hinglish) and the agent understands your intent, checks availability, negotiates an alternative if your slot is taken, and confirms the booking — all in voice.

**🔗 Live demo:** https://sarvam-voice-agent-xsc1.onrender.com
*(Free tier — first load may take ~50s while the server wakes up.)*

---

## What it does

Speak: *"Mujhe Tuesday shaam 6 baje appointment book karna hai."*

The agent:
1. **Transcribes** your speech (Saaras STT)
2. **Understands** intent — extracts action, day, and time as structured data (Sarvam-105B)
3. **Acts** — checks a calendar, and if the slot is taken, offers the next available one
4. **Responds** in natural Hindi voice (Bulbul TTS)
5. **Remembers** the conversation — say "Haan" and it books the offered slot

This is the core **perceive → understand → act → respond** loop that production voice agents run at scale.

---

## Architecture
