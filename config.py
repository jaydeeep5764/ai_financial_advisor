import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Attempt to configure the Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY and GEMINI_API_KEY != "your_api_key_here":
    print("API Key found. Configuring Gemini...")
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("WARNING: GEMINI_API_KEY not found or is default in .env file.")
    print("Please set your API key to enable AI features.")

def get_gemini_model(model_name="gemini-2.5-flash"):
    """
    Returns an instance of the GenerativeModel.
    Defaulting to gemini-2.5-flash which is generally fast and capable.
    """
    return genai.GenerativeModel(model_name)
