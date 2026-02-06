# ==============================
# main.py - FastAPI Backend
# ==============================

import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from groq import Groq

# Load environment variables
load_dotenv()

# -----------------------------
# Database Imports
# -----------------------------
from backend.database import engine, Base, SessionLocal
from backend import models, crud
from backend.config import settings  # GROQ API key & model settings

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
# Root Endpoint
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

# -----------------------------
# Chat Endpoint
# -----------------------------
@app.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    """
    Chat endpoint with:
    - Last N message context
    - System prompt
    - Timestamped AI response
    """

    # 1️⃣ Get or create user
    user = crud.get_or_create_user(db, req.google_id, req.email, req.name)

    # 2️⃣ Save user message
    crud.save_message(db, user.id, "user", req.message)

    # 3️⃣ Fetch full chat history
    history = crud.get_chat_history(db, user.id)

    # 4️⃣ Limit messages to last N for context
    N = 10  # You can adjust this number
    last_messages = history[-N:]

    # Convert DB messages to LLM format
    messages = [{"role": m.role, "content": m.content} for m in last_messages]

    # 5️⃣ Optional system prompt (tells AI how to behave)
    system_prompt = {
        "role": "system",
        "content": "You are a helpful assistant that remembers previous messages and answers concisely."
    }

    # Add system prompt at the start
    messages = [system_prompt] + messages

    # 6️⃣ Call LLM
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    reply = response.choices[0].message.content

    # 7️⃣ Save assistant reply
    crud.save_message(db, user.id, "assistant", reply)

    # 8️⃣ Return response with timestamp
    return {
        "response": reply,
        "timestamp": str(history[-1].timestamp)  # latest user message timestamp
    }

# -----------------------------
# Fetch User Chat History
# -----------------------------
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
