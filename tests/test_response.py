# tests/test_response.py

import pytest
from app.main import generate_gemini_response

def test_generate_response_valid_prompt():
    prompt = "Tell me a joke"
    response = generate_gemini_response(prompt)
    assert "Response for" in response
    assert prompt in response

def test_generate_response_empty_prompt():
    prompt = ""
    response = generate_gemini_response(prompt)
    assert response == "Prompt is empty"
