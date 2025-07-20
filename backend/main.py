from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# CORS untuk frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

# === SETTING ===
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # Di-set di Render Dashboard (Environment Variable)
MODEL = "openchat/openchat-3.5"  # Atau ganti model lain: "meta-llama/llama-3-8b-instruct", "mistralai/mistral-7b-instruct", dst.

@app.post("/chat")
async def chat(msg: Message):
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": msg.message}],
        "stream": False
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://chatbot-ai-openchat.onrender.com/",  # domain
        "X-Title": "Chatbot AI by Ikhsan"           # Nama project kamu
    }

    try:
        response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return {
            "response": data['choices'][0]['message']['content']
        }
    except Exception as e:
        return {"error": str(e)}
