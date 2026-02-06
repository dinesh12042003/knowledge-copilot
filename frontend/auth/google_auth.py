import streamlit as st
import jwt
from streamlit_oauth import OAuth2Component
from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
REVOKE_URL = "https://oauth2.googleapis.com/revoke"

oauth2 = OAuth2Component(
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    AUTHORIZE_URL,
    TOKEN_URL,
    TOKEN_URL,
    REVOKE_URL,
)


def login():
    result = oauth2.authorize_button(
        name="Login with Google",
        redirect_uri="http://localhost:8501",
        scope="openid email profile",
        key="google",
    )

    if result and "token" in result:

        token = result["token"]
        id_token = token["id_token"]

        # Decode token WITHOUT verification (safe enough for local project)
        decoded = jwt.decode(id_token, options={"verify_signature": False})

        st.session_state["user"] = {
            "email": decoded.get("email"),
            "name": decoded.get("name"),
            "id": decoded.get("sub"),
        }

        st.session_state["logged_in"] = True


def logout():
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()
