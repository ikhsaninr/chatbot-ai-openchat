from fastapi import FastAPI, Request
from pydantic import BaseModel
import os
import requests

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
REFERER = os.environ.get("REFERER", "https://chatbot-ai-openchat.onrender.com")
TITLE = os.environ.get("TITLE", "OpenChat AI")

@app.get("/")
def root():
    return {"message": "Chatbot API is running!"}

@app.post("/chat")
def chat(request: ChatRequest):
    if not OPENROUTER_API_KEY:
        return {"error": "OPENROUTER_API_KEY is not set in the environment variables."}

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": REFERER,
        "X-Title": TITLE,
        "Content-Type": "application/json",
    }

    data = {
        "model": "openai/gpt-4o",
        "messages": [
            {"role": "user", "content": request.message}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}
