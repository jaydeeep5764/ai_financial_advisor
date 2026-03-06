import streamlit as st

import pandas as pd
import json
import google.generativeai as genai
import os
from dotenv import load_dotenv
from financial_analysis import analyze_finances


from config import get_gemini_model, GEMINI_API_KEY
from finance_analysis import generate_financial_summary
from ai_advisor import generate_financial_advice, ask_chatbot
from visualization import create_savings_vs_expenses_chart, create_emergency_fund_progress_bar
from utils import format_currency, split_advice_into_sections

# Setup Streamlit page configuration
st.set_page_config(
    page_title="FinAI - Your AI Financial Advisor",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Load Custom CSS
def load_css():

model = genai.GenerativeModel("gemini-2.0-flash")

st.title("AI Financial Advisor")
result = analyze_finances(user_data)
st.write(result)
question = st.text_input("Ask a financial question")

if question:

    try:
        with open("styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css()

# Session State Initialization
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if 'financial_plan' not in st.session_state:
    st.session_state['financial_plan'] = None

def render_metric_card(label, value, condition_class="neutral"):
    html = f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value {condition_class}">{value}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# Application Header
st.title("💡 FinAI Advisor")
st.markdown("Your personalized, AI-driven financial dashboard and planning assistant.")

if not GEMINI_API_KEY or GEMINI_API_KEY == "your_api_key_here":
    st.error("⚠️ Gemini API Key is missing. Please add it to your `.env` file to enable AI features.")

# Sidebar - User Inputs
st.sidebar.header("📊 Financial Profile Input")

with st.sidebar.form("financial_form"):
    st.subheader("Monthly Cash Flow")
    income = st.number_input("Monthly Income ($)", min_value=0.0, value=5000.0, step=100.0)
    expenses = st.number_input("Monthly Expenses ($)", min_value=0.0, value=3000.0, step=100.0)
    savings = st.number_input("Monthly Savings/Investments ($)", min_value=0.0, value=1000.0, step=100.0)
    debt_payments = st.number_input("Monthly Debt Payments ($)", min_value=0.0, value=500.0, step=100.0)
    
    st.subheader("Assets")
    current_ef = st.number_input("Current Emergency Fund ($)", min_value=0.0, value=10000.0, step=500.0)
    
    st.subheader("Preferences")
    risk_tolerance = st.selectbox("Risk Tolerance", ["Conservative", "Moderate", "Aggressive"])
    
    st.subheader("Financial Goals")
    goals_text = st.text_area("List your top financial goals (one per line)", "Build an emergency fund\nSave for a house downpayment")
    goals_list = [g.strip() for g in goals_text.split('\n') if g.strip()]
    
    submit_button = st.form_submit_button("Generate Financial Summary")

# On Submit
if submit_button:
    summary = generate_financial_summary(income, expenses, savings, debt_payments, current_ef)
    st.session_state['summary'] = summary
    st.session_state['risk_tolerance'] = risk_tolerance
    st.session_state['goals_list'] = goals_list
    # Reset financial plan to regenerate it when requested
    st.session_state['financial_plan'] = None


# Display Dashboard if Summary Exists
if 'summary' in st.session_state:
    summary = st.session_state['summary']
    
    tab1, tab2, tab3 = st.tabs(["📈 Financial Dashboard", "🤖 AI Financial Plan", "💬 FinAI Chat"])
    
    with tab1:
        st.header("Financial Overview")
        
        # Metrics Top Row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            render_metric_card("Disposable Income", format_currency(summary['disposable_income']), "good" if summary['disposable_income'] > 0 else "critical")
        with col2:
            s_class = "good" if summary['savings_ratio'] >= 20 else "warning" if summary['savings_ratio'] > 0 else "critical"
            render_metric_card("Savings Ratio", f"{summary['savings_ratio']}%", s_class)
        with col3:
            d_class = "good" if summary['dti_ratio'] <= 35 else "warning" if summary['dti_ratio'] <= 43 else "critical"
            render_metric_card("Debt-to-Income", f"{summary['dti_ratio']}%", d_class)
        with col4:
            e_class = "good" if summary['emergency_fund_months_covered'] >= 6 else "warning" if summary['emergency_fund_months_covered'] >= 3 else "critical"
            render_metric_card("Emergency Fund", f"{summary['emergency_fund_months_covered']} mo", e_class)

        st.markdown("<hr/>", unsafe_allow_html=True)
        
        st.subheader("Visual Analysis")
        colA, colB = st.columns(2)
        with colA:
            st.markdown("**Income Allocation**")
            fig1 = create_savings_vs_expenses_chart(summary['monthly_income'], summary['monthly_expenses'], summary['monthly_savings'], summary['monthly_debt_payments'])
            st.pyplot(fig1)
        with colB:
            st.markdown("**Emergency Fund Progress**")
            st.markdown(f"Target: **{format_currency(summary['emergency_fund_target'])}** (6 months expenses)")
            fig2 = create_emergency_fund_progress_bar(summary['emergency_fund_current'], summary['emergency_fund_target'])
            st.pyplot(fig2)
            st.info(f"Status: {summary['emergency_fund_status']}")

    with tab2:
        st.header("Your Personalized AI Financial Plan")
        
        if st.button("Generate AI Plan", use_container_width=True):
            with st.spinner("FinAI is analyzing your profile..."):
                advice_md = generate_financial_advice(summary, st.session_state['risk_tolerance'], st.session_state['goals_list'])
                st.session_state['financial_plan'] = advice_md
                
        if st.session_state['financial_plan']:
            sections = split_advice_into_sections(st.session_state['financial_plan'])
            for sec in sections:
                st.markdown(f"<div class='advice-section'><h3>{sec['title']}</h3><p>{sec['content']}</p></div>", unsafe_allow_html=True)

    with tab3:
        st.header("Chat with FinAI")
        st.markdown("Ask specific questions about your finances, budget, or investment strategies.")
        
        # Display chat history
        for msg in st.session_state['chat_history']:
            if msg.role == 'user':
                st.chat_message("user").markdown(msg.parts[0].text)
            else:
                st.chat_message("assistant").markdown(msg.parts[0].text)
                
        # Chat Input
        if prompt := st.chat_input("Ask FinAI... e.g. 'How can I lower my debt faster?'"):
            st.chat_message("user").markdown(prompt)
            
            with st.spinner("FinAI is thinking..."):
                response_text, updated_history = ask_chatbot(st.session_state['chat_history'], prompt, summary)
                st.session_state['chat_history'] = updated_history
                
                st.chat_message("assistant").markdown(response_text)
else:
    st.info("👈 Please enter your financial details in the sidebar and click **Generate Financial Summary** to begin.")
