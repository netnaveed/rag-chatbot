import streamlit as st
import requests

# API endpoint of the chatbot
CHATBOT_API_URL = "http://localhost:5000/chat"

st.set_page_config(page_title="Chatbot", page_icon="🤖")
st.title("💬 Creative Chaos Bot")
st.write("Ask me anything about the company playbook!")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask me anything about the company...")

if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send request to chatbot API
    try:
        response = requests.post(CHATBOT_API_URL, json={"query": user_input})
        if response.status_code == 200:
            bot_reply = response.json().get("response", "I couldn't understand that.")
        else:
            bot_reply = f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        bot_reply = f"Connection error: {e}"

    # Display chatbot response
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
