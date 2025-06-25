import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load the API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Set page title
st.set_page_config(page_title="GPT-4 Chatbot with Memory", layout="centered")
st.title("🧠 GPT-4 Chatbot with Memory")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat messages
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**AI:** {msg['content']}")

# Input area
user_input = st.text_area("Your message", height=100, key="input")

# Trigger on button
if st.button("Send"):
    try:
        # Add current user message to session memory
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Call OpenAI with full conversation
        response = client.chat.completions.create(
            model="gpt-4",
            messages=st.session_state.chat_history
        )

        # Extract and append assistant reply
        reply = response.choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        # Force rerun to refresh UI
        st.rerun()

    except Exception as e:
        st.error(f"Error: {e}")
