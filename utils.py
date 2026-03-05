import re

def format_currency(value):
    """Format a numeric value as currency (e.g., $1,234.56)."""
    try:
        return f"${float(value):,.2f}"
    except (ValueError, TypeError):
        return "$0.00"

def format_percentage(value):
    """Format a numeric value as a percentage (e.g., 12.3%)."""
    try:
        return f"{float(value):.1f}%"
    except (ValueError, TypeError):
        return "0.0%"
        
def parse_numeric_input(value_str):
    """Safely parse user string inputs into floats."""
    if not value_str:
        return 0.0
    
    # Remove currency symbols and commas
    clean_str = re.sub(r'[^\d.]', '', str(value_str))
    try:
        return float(clean_str)
    except ValueError:
        return 0.0

def split_advice_into_sections(markdown_text):
    """Split markdown text from Gemini into logical chunks based on headers."""
    # Split by H2 or H3 headers
    sections = re.split(r'\n(##+ .*)', markdown_text)
    
    result = []
    current_title = "General Advice"
    current_content = ""
    
    if sections and not sections[0].startswith('##'):
        current_content = sections[0].strip()
        if current_content:
            result.append({"title": current_title, "content": current_content})
            
    for i in range(1, len(sections), 2):
        title = sections[i].strip("#").strip()
        content = sections[i+1].strip() if i+1 < len(sections) else ""
        if content:
             result.append({"title": title, "content": content})
             
    # Fallback if no headers were found
    if not result and markdown_text.strip():
        result.append({"title": "Financial Recommendations", "content": markdown_text.strip()})
        
    return result
