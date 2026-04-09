import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# UPDATED MODEL CONFIG (IMPORTANT)
model = genai.GenerativeModel(
    "gemini-2.5-flash",
    generation_config={
        "max_output_tokens": 1600,
        "temperature": 0.7
    }
)

def generate_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text if response.text else "No response generated."
    except Exception as e:
        return "Server busy. Try again later."