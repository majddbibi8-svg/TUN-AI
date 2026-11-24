import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from huggingface_hub import InferenceClient

load_dotenv()
app = FastAPI(title="TUN AI")
app.mount("/static", StaticFiles(directory="static"), name="static")

class ChatRequest(BaseModel):
    message: str
    language: str = "en"

@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.get("/api/wiki")
def wiki_search(q: str, lang: str = "en"):
    lang = lang if lang in {"en", "fr", "ar"} else "en"
    try:
        url = f"https://{lang}.wikipedia.org/w/api.php"
        response = requests.get(url, params={
            "action": "query", "list": "search", "srsearch": q,
            "format": "json", "utf8": 1, "srlimit": 8
        }, timeout=15, headers={"User-Agent": "TUN-AI/1.0"})
        response.raise_for_status()
        results = response.json().get("query", {}).get("search", [])
        return {"results": [{
            "title": x["title"],
            "snippet": x.get("snippet", ""),
            "url": f"https://{lang}.wikipedia.org/wiki/" + requests.utils.quote(x["title"].replace(" ", "_"))
        } for x in results]}
    except requests.RequestException:
        raise HTTPException(status_code=502, detail="Wikipedia search is temporarily unavailable.")

@app.post("/api/chat")
def chat(body: ChatRequest):
    token = os.getenv("HF_TOKEN")
    if not token or token == "put_your_huggingface_token_here":
        raise HTTPException(status_code=503, detail="AI is not configured yet. Add HF_TOKEN to the server environment.")
    model = os.getenv("HF_MODEL", "Qwen/Qwen2.5-7B-Instruct")
    language_names = {"en": "English", "fr": "French", "ar": "Arabic"}
    language = language_names.get(body.language, "English")
    try:
        client = InferenceClient(model=model, token=token)
        answer = client.chat_completion(
            messages=[
                {"role": "system", "content": f"You are TUN AI, a helpful encyclopedia assistant. Answer accurately and clearly in {language}. If unsure, say so. Distinguish facts from uncertainty."},
                {"role": "user", "content": body.message}
            ],
            max_tokens=700,
            temperature=0.5
        )
        return {"answer": answer.choices[0].message.content}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"AI provider error: {str(exc)[:240]}")
