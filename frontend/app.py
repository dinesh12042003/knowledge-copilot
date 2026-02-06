# ==============================
# app.py - Streamlit Frontend
# ==============================

import streamlit as st
import requests
from datetime import datetime
from auth.google_auth import login, logout

# -----------------------------
# Backend Endpoint
# -----------------------------
BACKEND_URL = "https://knowledge-copilot-mo21.onrender.com"

# -----------------------------
# Page Configuration
# Must be first Streamlit command
# -----------------------------
st.set_page_config(
    page_title="Knowledge Copilot",
    page_icon="🧠",
    layout="wide"
)

# -----------------------------
# Authentication Gate
# -----------------------------
if "logged_in" not in st.session_state:
    login()
    st.stop()  # stop until user logs in

user = st.session_state["user"]  # current logged-in user

# -----------------------------
# Initialize chat session state
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Fetch history from backend on login
# -----------------------------
try:
    history_resp = requests.get(
        f"{BACKEND_URL.replace('/chat','/history')}/{user['id']}"
    )
    if history_resp.status_code == 200:
        st.session_state.messages = history_resp.json().get("messages", [])
except Exception as e:
    st.warning(f"Could not load history: {e}")

# -----------------------------
# Context window for LLM
# -----------------------------
CONTEXT_WINDOW = 10  # Only last N messages will be sent to AI
messages_to_send = st.session_state.messages[-CONTEXT_WINDOW:]

# -----------------------------
# Sidebar: User Controls
# -----------------------------
with st.sidebar:
    st.title("⚙️ Control Panel")
    st.success("Logged in as")
    st.write(f"**{user['name']}**")
    st.caption(user["email"])

    # Reset chat
    if st.button("🔄 Reset Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    # Developer / Debug mode toggle
    show_debug = st.toggle("Developer Mode")

    st.divider()

    # Logout
    if st.button("🚪 Logout"):
        logout()
        st.rerun()

# -----------------------------
# Main Page Header
# -----------------------------
st.title("🧠 Personal Knowledge Copilot")
st.caption("Your AI that remembers, assists, and grows with you")

# -----------------------------
# Display chat history
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "time" in message:
            st.caption(message["time"])

# -----------------------------
# User Input
# -----------------------------
prompt = st.chat_input("Ask me anything...")

# -----------------------------
# Handle User Prompt
# -----------------------------
if prompt:
    # Timestamp for user message
    timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
            "time": timestamp
        }
    )

    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(timestamp)

    # -----------------------------
    # Call backend for AI response
    # -----------------------------
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    BACKEND_URL,
                    json={
                        "google_id": user["id"],
                        "email": user["email"],
                        "name": user["name"],
                        "message": prompt
                    },
                    timeout=60
                )

                if response.status_code == 200:
                    data = response.json()
                    reply = data.get("response", "No response from AI")
                    ai_timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")
                else:
                    reply = f"Backend Error {response.status_code}"
                    ai_timestamp = None

            except Exception as e:
                reply = f"Connection failed:\n{str(e)}"
                ai_timestamp = None

        # Display AI reply
        st.markdown(reply)
        if ai_timestamp:
            st.caption(ai_timestamp)

    # Save AI reply to session state
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply,
            "time": ai_timestamp
        }
    )

# -----------------------------
# Developer / Debug Panel
# -----------------------------
if show_debug:
    st.divider()
    st.subheader("🧪 Debug Info")
    st.json({
        "session_state_keys": list(st.session_state.keys()),
        "messages_count": len(st.session_state.messages),
        "backend_url": BACKEND_URL
    })
