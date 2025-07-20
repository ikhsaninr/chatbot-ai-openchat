from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

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

OLLAMA_API_URL = "http://localhost:11434/api/chat"
MODEL = "openchat"  # Bisa diganti 'llama3', 'mistral', dll

@app.post("/chat")
async def chat(msg: Message):
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": msg.message}],
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return {"response": data.get("message", {}).get("content", "")}
    except Exception as e:
        return {"error": str(e)}
