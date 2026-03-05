from config import get_gemini_model
import json

def generate_financial_advice(financial_summary, risk_tolerance, goals_list):
    """
    Calls the Gemini API to produce an initial assessment based on the user's
    computed financial profile.
    """
    model = get_gemini_model()
    
    # Format the input data for the LLM
    prompt = f"""
    You are an expert AI Financial Advisor. Based on the user's financial summary, risk tolerance, and goals, provide actionable advice.
    
    User Financial Profile:
    - Monthly Income: ${financial_summary['monthly_income']}
    - Monthly Expenses: ${financial_summary['monthly_expenses']}
    - Monthly Savings: ${financial_summary['monthly_savings']} (Ratio: {financial_summary['savings_ratio']}%, Status: {financial_summary['savings_status']})
    - Monthly Debt Payments: ${financial_summary['monthly_debt_payments']} (DTI Ratio: {financial_summary['dti_ratio']}%, Status: {financial_summary['dti_status']})
    - Unallocated/Disposable Income: ${financial_summary['disposable_income']}
    
    Emergency Fund:
    - Current: ${financial_summary['emergency_fund_current']}
    - Target: ${financial_summary['emergency_fund_target']}
    - Status: {financial_summary['emergency_fund_status']} ({financial_summary['emergency_fund_months_covered']} months covered)
    
    Risk Tolerance: {risk_tolerance}
    
    Stated Goals:
    {json.dumps(goals_list, indent=2)}
    
    Please provide your advice structured with clear Markdown headers (##) for the following sections:
    ## Immediate Actions (Next 30 Days)
    ## Budget Optimization
    ## Debt Management Strategy (if applicable, else skip)
    ## Investment & Growing Wealth (tailored to their {risk_tolerance} risk tolerance)
    ## Path to Goals
    
    Keep the tone professional, encouraging, and clear. Do not provide certified financial planning advice in a legal sense, but do offer robust best-practices.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error connecting to AI Advisor: {str(e)}\n\nPlease ensure your Gemini API key is configured correctly."

def ask_chatbot(chat_history, new_user_message, financial_summary):
    """
    Handles a conversational turn with the Gemini AI, providing context of the user's finances.
    chat_history should be a list of dicts: [{'role': 'user'/'model', 'parts': ['text']}]
    """
    model = get_gemini_model()
    
    # We initialize a chat session using the model. 
    # To keep the system prompt contextual, we'll embed the summary into a hidden initial system instruction or just prepend it to the first message if system instructions aren't supported.
    
    system_context = f"""
    You are a helpful AI Financial Advisor. You have the following context about the user's finances:
    Income: ${financial_summary.get('monthly_income', 0)}, Expenses: ${financial_summary.get('monthly_expenses', 0)},
    Savings Ratio: {financial_summary.get('savings_ratio', 0)}%, DTI Ratio: {financial_summary.get('dti_ratio', 0)}%.
    Keep your answers concise, practical, and conversational.
    """
    
    # We use Google's genai ChatSession feature.
    try:
        # Start chat with history
        chat = model.start_chat(history=chat_history)
        
        # If this is a very new conversation, inject system context
        if len(chat_history) == 0:
             full_message = f"System Context: {system_context}\n\nUser Question: {new_user_message}"
        else:
             full_message = new_user_message
             
        response = chat.send_message(full_message)
        
        # Return the raw text and the updated history list
        return response.text, chat.history
        
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}", chat_history
