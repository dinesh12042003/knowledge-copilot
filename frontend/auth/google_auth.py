import streamlit as st
import requests
from requests_oauthlib import OAuth2Session

# -----------------------------
# CONFIG
# -----------------------------
CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]
CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]

REDIRECT_URI = st.secrets.get(
    "REDIRECT_URI",
    "http://localhost:8501"
)

AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"

SCOPE = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

# -----------------------------
# LOGIN
# -----------------------------
def login():

    # Already logged in
    if "logged_in" in st.session_state:
        return

    # OAuth session
    oauth = OAuth2Session(
        CLIENT_ID,
        scope=SCOPE,
        redirect_uri=REDIRECT_URI
    )

    # Step A — If we received code from Google
    query = st.query_params

    if "code" in query:

        token = oauth.fetch_token(
            TOKEN_URL,
            client_secret=CLIENT_SECRET,
            code=query["code"]
        )

        # Get user info
        resp = oauth.get(USERINFO_URL)
        user_info = resp.json()

        # Save to session
        st.session_state.logged_in = True
        st.session_state.user = {
            "id": user_info["id"],
            "email": user_info["email"],
            "name": user_info["name"],
        }

        st.query_params.clear()
        st.rerun()

    # Step B — Start login flow
    else:
        authorization_url, state = oauth.authorization_url(
            AUTH_URL,
            access_type="offline",
            prompt="select_account"
        )

        st.markdown(
            f"""
            ### 🔐 Login Required
            [👉 Login with Google]({authorization_url})
            """,
            unsafe_allow_html=True
        )


# -----------------------------
# LOGOUT
# -----------------------------
def logout():
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()
