import os
import time
from collections import defaultdict
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import APIKeyHeader
from pydantic import BaseModel

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from query.rag_pipeline import ask

app = FastAPI(title="Medicare/Medicaid Policy Chatbot API")

API_KEY        = os.getenv("CHATBOT_API_KEY", "demo-key-12345")
api_key_header = APIKeyHeader(name="X-API-Key")

# Simple in-memory rate limiter: max 10 requests per 60s per key
_rate_store: dict[str, list[float]] = defaultdict(list)
RATE_LIMIT    = 10
RATE_WINDOW   = 60


def verify_api_key(key: str = Depends(api_key_header)):
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return key


def rate_limit(request: Request, key: str = Depends(verify_api_key)):
    now = time.time()
    timestamps = _rate_store[key]
    _rate_store[key] = [t for t in timestamps if now - t < RATE_WINDOW]
    if len(_rate_store[key]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Max 10 requests per minute.")
    _rate_store[key].append(now)
    return key


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: list[str]


class CoverageResponse(BaseModel):
    procedure_code: str
    covered: bool
    notes: str
    sources: list[str]


@app.get("/health")
def health():
    return {"status": "ok", "service": "policy-chatbot"}


@app.post("/chat", response_model=ChatResponse)
def chat(body: ChatRequest, _: str = Depends(rate_limit)):
    if not body.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    result = ask(body.question)
    return ChatResponse(
        question=result["question"],
        answer=result["answer"],
        sources=result["sources"],
    )


@app.get("/coverage-check", response_model=CoverageResponse)
def coverage_check(procedure_code: str, _: str = Depends(rate_limit)):
    question = (
        f"Is procedure code {procedure_code} covered under Medicare or Medicaid? "
        f"What are the billing requirements and any prior authorization needed?"
    )
    result = ask(question)
    answer_lower = result["answer"].lower()
    covered = any(w in answer_lower for w in ["covered", "eligible", "reimburs", "billable"])
    return CoverageResponse(
        procedure_code=procedure_code,
        covered=covered,
        notes=result["answer"],
        sources=result["sources"],
    )
