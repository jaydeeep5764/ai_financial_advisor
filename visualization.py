import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io

def create_savings_vs_expenses_chart(income, expenses, savings, debt_payments):
    """Generates a pie chart of income allocation."""
    
    disposable = max(0, income - expenses - savings - debt_payments)
    
    labels = ['Expenses', 'Savings', 'Debt Payments', 'Disposable']
    values = [expenses, savings, debt_payments, disposable]
    
    # Filter out empty categories
    filtered_labels = [l for l, v in zip(labels, values) if v > 0]
    filtered_values = [v for v in values if v > 0]
    
    if not filtered_values:
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.text(0.5, 0.5, "No Data Provided", ha='center', va='center', fontsize=12)
        ax.axis('off')
        return fig
        
    colors = sns.color_palette("Set2")[:len(filtered_values)]
    
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(filtered_values, labels=filtered_labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    return fig

def create_emergency_fund_progress_bar(current_fund, target_fund):
    """Generates a bar chart showing emergency fund progress."""
    
    fig, ax = plt.subplots(figsize=(8, 2))
    
    if target_fund <= 0:
        ax.text(0.5, 0.5, "Target fund not set or zero.", ha='center', va='center')
        ax.axis('off')
        return fig
        
    progress = min(current_fund / target_fund, 1.0)
    
    # Draw background bar (target)
    ax.barh(0, 1.0, color='#e0e0e0', height=0.5)
    
    # Draw foreground bar (current progress)
    color = '#4caf50' if progress >= 1.0 else '#ff9800' if progress >= 0.5 else '#f44336'
    ax.barh(0, progress, color=color, height=0.5)
    
    # Formatting
    ax.set_xlim(0, 1.0)
    ax.set_ylim(-0.5, 0.5)
    ax.axis('off')
    
    return fig
