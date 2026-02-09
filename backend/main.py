# ==============================
# main.py - FastAPI Backend
# ==============================

import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from groq import Groq
from pathlib import Path

# -----------------------------
# Load environment variables
# -----------------------------


env_path = Path(__file__).parent.parent / ".env"
load_dotenv(override=True)


# -----------------------------
# Database Imports
# -----------------------------
from backend.database import engine, Base, SessionLocal
from backend import models, crud
from backend.config import settings  # GROQ API key & model settings

# -----------------------------
# RAG Imports
# -----------------------------
from backend.rag.retriever import retrieve_context

# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI(title="Knowledge Copilot Backend 🚀")

# -----------------------------
# Create Tables
# -----------------------------
Base.metadata.create_all(bind=engine)

# -----------------------------
# Dependency: DB Session
# -----------------------------
def get_db():
    """Provide a transactional scope around DB operations."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# GROQ LLM Client Setup
# -----------------------------
client = Groq(api_key=settings.GROQ_API_KEY)
MODEL = settings.MODEL

# -----------------------------
# Request Schema
# -----------------------------
class ChatRequest(BaseModel):
    google_id: str
    email: str
    name: str
    message: str

# -----------------------------
# Root Endpoint (Health Check)
# -----------------------------
@app.get("/")
def root():
    """Simple health check"""
    return {"status": "Backend running 🚀"}

# -----------------------------
# Test Database Endpoint
# -----------------------------
@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    """Test DB functionality: create user, save message, fetch history."""
    user = crud.get_or_create_user(
        db,
        google_id="test123",
        email="test@mail.com",
        name="Tester"
    )

    crud.save_message(db, user.id, role="user", content="Hello DB!")

    history = crud.get_chat_history(db, user.id)

    return {
        "messages": [
            {
                "role": m.role,
                "content": m.content,
                "time": str(m.timestamp)
            }
            for m in history
        ]
    }

# =============================
# Chat Endpoint
# =============================
@app.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    """
    Chat endpoint with:
    - SQL memory (user messages)
    - RAG knowledge retrieval (global + user docs)
    - System behavior prompt
    - Timestamped assistant response
    """

    # 1️⃣ Get or create user in DB
    user = crud.get_or_create_user(
        db, req.google_id, req.email, req.name
    )

    # 2️⃣ Save incoming user message
    crud.save_message(db, user.id, "user", req.message)

    # 3️⃣ Fetch user chat history from DB
    history = crud.get_chat_history(db, user.id)

    # 4️⃣ Limit to last N messages for context window
    N = 10
    last_messages = history[-N:]
    messages = [{"role": m.role, "content": m.content} for m in last_messages]

    # 5️⃣ Retrieve RAG context: global + user-specific docs
    context, sources = retrieve_context(
        user_query=req.message,
        user_id=req.google_id
    )

    # 6️⃣ System prompt with retrieved context
    #    LLM sees both system instructions and context
    system_prompt = {
        "role": "system",
        "content": f"""
You are a helpful personal knowledge assistant.

Use the provided CONTEXT if relevant.
If context doesn't contain answer, respond normally.

CONTEXT:
{context}
"""
    }

    # 7️⃣ Combine system prompt with last user messages
    messages = [system_prompt] + messages

    # 8️⃣ Call LLM via GROQ API
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    # Extract assistant reply
    reply = response.choices[0].message.content

    # 9️⃣ Save assistant reply to DB
    crud.save_message(db, user.id, "assistant", reply)

    # 🔟 Return reply + sources + timestamp
    return {
        "response": reply,
        "sources": sources,
        "timestamp": str(history[-1].timestamp)
    }

# =============================
# Fetch User Chat History
# =============================
@app.get("/history/{google_id}")
def get_history(google_id: str, db: Session = Depends(get_db)):
    """
    Return all chat messages for a specific user.
    If user not found, return empty list.
    """
    user = crud.get_user_by_google_id(db, google_id)
    if not user:
        return {"messages": []}

    history = crud.get_chat_history(db, user.id)

    return {
        "messages": [
            {
                "role": m.role,
                "content": m.content,
                "time": str(m.timestamp)
            }
            for m in history
        ]
    }
