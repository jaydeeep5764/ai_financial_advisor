import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

st.title("AI Financial Advisor")

question = st.text_input("Ask a financial question")

if question:
    try:
        response = model.generate_content(question)
        st.write(response.text)
    except Exception as e:
        st.error("API limit reached or error occurred. Try again later.")