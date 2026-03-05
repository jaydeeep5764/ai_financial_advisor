def calculate_savings_ratio(income, savings):
    """Calculate the ratio of savings to income."""
    if income <= 0:
        return 0, "No income reported."
    ratio = (savings / income) * 100
    
    if ratio >= 20:
        status = "Excellent"
    elif ratio >= 10:
        status = "Good"
    elif ratio > 0:
        status = "Needs Improvement"
    else:
        status = "Critical - No savings"
        
    return ratio, status

def calculate_debt_to_income_ratio(income, debt_payments):
    """Calculate the debt-to-income (DTI) ratio."""
    if income <= 0:
        return 0, "No income reported."
    
    ratio = (debt_payments / income) * 100
    
    if ratio <= 20:
        status = "Excellent"
    elif ratio <= 35:
        status = "Good"
    elif ratio <= 43:
        status = "Warning - High Debt"
    else:
        status = "Critical - Excessive Debt"
        
    return ratio, status

def calculate_emergency_fund_needs(monthly_expenses, target_months=6):
    """Calculate required emergency fund amount."""
    target_amount = monthly_expenses * target_months
    return target_amount

def evaluate_emergency_fund(current_fund, monthly_expenses, target_months=6):
    """Evaluate current emergency fund status."""
    target_amount = calculate_emergency_fund_needs(monthly_expenses, target_months)
    
    if target_amount == 0:
        return 0, 0, "No expenses reported."
        
    progress = (current_fund / target_amount) * 100
    progress = min(progress, 100) # Cap at 100%
    
    months_covered = current_fund / monthly_expenses if monthly_expenses > 0 else 0
    
    if months_covered >= 6:
        status = "Excellent - Fully Funded"
    elif months_covered >= 3:
        status = "Good - Partially Funded"
    elif months_covered > 0:
        status = "Needs Improvement - Low Funds"
    else:
        status = "Critical - No Emergency Fund"
        
    return progress, months_covered, status
    
def generate_financial_summary(income, expenses, savings, debt_payments, current_emergency_fund):
    """Generate a comprehensive dictionary summarizing the financial status."""
    
    savings_ratio, savings_status = calculate_savings_ratio(income, savings)
    dti_ratio, dti_status = calculate_debt_to_income_ratio(income, debt_payments)
    ef_progress, ef_months, ef_status = evaluate_emergency_fund(current_emergency_fund, expenses)
    
    disposable_income = income - expenses - savings - debt_payments
    
    return {
        "monthly_income": income,
        "monthly_expenses": expenses,
        "monthly_savings": savings,
        "monthly_debt_payments": debt_payments,
        "disposable_income": disposable_income,
        "savings_ratio": round(savings_ratio, 2),
        "savings_status": savings_status,
        "dti_ratio": round(dti_ratio, 2),
        "dti_status": dti_status,
        "emergency_fund_current": current_emergency_fund,
        "emergency_fund_target": calculate_emergency_fund_needs(expenses),
        "emergency_fund_progress": round(ef_progress, 2),
        "emergency_fund_months_covered": round(ef_months, 1),
        "emergency_fund_status": ef_status
    }
