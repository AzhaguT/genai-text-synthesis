import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# Add the path to access app/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

import main

def test_load_api_key(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "dummy_key")
    result = os.getenv("GOOGLE_API_KEY")
    assert result == "dummy_key"

def test_configure_genai_valid():
    with patch("google.generativeai.configure") as mock_config:
        main.configure_genai("valid_key")
        mock_config.assert_called_once_with(api_key="valid_key")

def test_configure_genai_invalid():
    with pytest.raises(ValueError):
        main.configure_genai(None)

def test_init_model():
    with patch("google.generativeai.GenerativeModel") as MockModel:
        main.init_model()
        MockModel.assert_called_once_with(model_name="models/gemini-2.0-pro-exp")

def test_start_chat_session():
    model = MagicMock()
    mock_chat = MagicMock()
    model.start_chat.return_value = mock_chat

    # Simulate Streamlit session state
    import streamlit as st
    st.session_state.clear()
    main.start_chat_session(model)

    assert "chat" in st.session_state
    assert st.session_state.chat == mock_chat

def test_generate_gemini_response():
    mock_model = MagicMock()
    mock_model.generate_content.return_value.text = "Mock reply"
    result = main.generate_gemini_response("Hello", mock_model)
    assert result == "Mock reply"
