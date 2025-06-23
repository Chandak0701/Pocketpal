import streamlit as st
import requests

OLLAMA_MODEL = "llama3"

OLLAMA_API_URL = "http://localhost:11434/api/generate"

st.set_page_config(page_title="PocketPal AI", layout="centered")

st.title("🤖 PocketPal — Chat with Local AI")
st.caption(f"Powered by Ollama • Model: `{OLLAMA_MODEL}`")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.chat_input("Ask something...")
if user_input:
    st.session_state.history.append(("user", user_input))

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": user_input,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        answer = result.get("response", "❌ No response")
    except Exception as e:
        answer = f"Error: {str(e)}"

    st.session_state.history.append(("bot", answer))

for role, msg in st.session_state.history:
    with st.chat_message("user" if role == "user" else "assistant"):
        st.markdown(msg)
