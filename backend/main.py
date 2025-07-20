from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

# Konfigurasi CORS (jika ingin akses dari frontend domain lain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ubah ke asal tertentu jika ingin lebih aman
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ganti ini dengan API key milikmu sendiri
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") 

@app.get("/")
def root():
    return {"message": "Chatbot API is running!"}

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_message = body.get("message")

    if not user_message:
        return {"error": "No message provided"}

    # Request ke OpenRouter API
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://chatbot-ai-openchat.onrender.com",  # domain
            "X-Title": "Chatbot AI OpenChat",  # judul aplikasi
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-4o",
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }
    )

    # Parsing respons
    try:
        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            reply = result["choices"][0]["message"]["content"]
            return {"reply": reply}
        else:
            return {"error": "Invalid response from OpenRouter", "raw": result}
    except Exception as e:
        return {"error": str(e), "raw_response": response.text}
