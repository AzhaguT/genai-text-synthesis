import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# You can also use an environment variable for safety
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Setup Gemini with your API key
genai.configure(api_key=GOOGLE_API_KEY)

models = genai.list_models()
for m in models:
    print(m.name, m.supported_generation_methods)

# Load the Gemini Pro model
model = genai.GenerativeModel(model_name="models/gemini-2.0-pro-exp")

# Initialize a chat session only once
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Streamlit UI
st.title("💬 Gemini Chatbot with Memory")

# Show chat history
for msg in st.session_state.chat.history:
    with st.chat_message(msg.role):
        st.markdown(msg.parts[0].text)

# User input
user_input = st.chat_input("Ask something...")        

if user_input:
    try:
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Send message to Gemini and get response
        response = st.session_state.chat.send_message(user_input)

            # Display Gemini's reply
        with st.chat_message("model"):
            st.markdown(response.text)
    except Exception as e:
        st.error(f"Error occurred: {e}")

