import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

class Message(BaseModel):
    message: str

@app.get("/")
def root():
    return {"message": "Chatbot API is running!"}

@app.post("/chat")
def chat(msg: Message):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://chatbot-ai-openchat.onrender.com",
        "X-Title": "Chatbot by Ikhsan"
    }

    payload = {
        "model": "openchat",
        "messages": [{"role": "user", "content": msg.message}],
        "stream": False
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
    return response.json()
