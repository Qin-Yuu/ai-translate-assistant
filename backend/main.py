import os
from dotenv import load_dotenv
load_dotenv()

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas import TranslateRequest, TranslateResponse
from llm_client import translate_with_llm

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("ai-translate-assistant")

app = FastAPI(title="AI Translate Assistant", version="1.0.0")

# Simple CORS so the demo UI can call the API.
# For production, restrict origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ALLOW_ORIGINS", "*").split(","),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/translate", response_model=TranslateResponse)
def translate(req: TranslateRequest):
    text = (req.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")
    if len(text) > int(os.getenv("MAX_TEXT_CHARS", "5000")):
        raise HTTPException(status_code=400, detail="text too long")

    try:
        result = translate_with_llm(text)
        return TranslateResponse(**result)
    except Exception as e:
        logger.exception("translate failed")
        raise HTTPException(status_code=500, detail=f"translate failed: {e}")
