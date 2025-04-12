import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv


def load_api_key():
    load_dotenv()
    # You can also use an environment variable for safety
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Setup Gemini with your API key
def configure_genai(api_key):
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment.")
    genai.configure(api_key=api_key)
'''
models = genai.list_models()
for m in models:
    print(m.name, m.supported_generation_methods)
'''

# Load the Gemini Pro model
def init_model():
    return genai.GenerativeModel(model_name="models/gemini-2.0-pro-exp")

# Initialize a chat session only once
def start_chat_session(model):
    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])

# Streamlit UI
st.title("💬 Gemini Chatbot with Memory")

# Show chat history
def display_chat_history():
    for msg in st.session_state.chat.history:
        with st.chat_message(msg.role):
            st.markdown(msg.parts[0].text)

def handle_user_input(user_input):
    try:
        with st.chat_message("user"):
            st.markdown(user_input)
        response = st.session_state.chat.send_message(user_input)
        with st.chat_message("model"):
            st.markdown(response.text)
    except Exception as e:
        st.error(f"Error occurred: {e}")

def generate_gemini_response(prompt, model):
    """
    Takes a user prompt and returns Gemini model's response.
    """
    return model.generate_content(prompt).text        

def main():
    st.title("💬 Gemini Chatbot with Memory")

    api_key = load_api_key()
    configure_genai(api_key)
    model = init_model()
    start_chat_session(model)
    display_chat_history()

    user_input = st.chat_input("Ask something...")
    if user_input:
        handle_user_input(user_input)

if __name__ == "__main__":
    main()

