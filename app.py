import os
import streamlit as st
import requests

API_KEY = os.getenv('OPENAI_API_KEY')

st.title("GPT Chatbot")

message = st.text_area("Enter your message:", "")

if st.button("Send"):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "inputs": message,
        "options": {
            "use_cache": False
        }
    }
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        reply = response.json()["generated_text"]
        st.text_area("Bot's reply:", reply, height=200)
    else:
        st.error(f"Failed to get response from the bot. Status code: {response.status_code}. Response: {response.text}")
