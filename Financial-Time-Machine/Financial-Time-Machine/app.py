#!/usr/bin/env python3
"""
Financial Time Machine - Main Application
"""
import sys
import matplotlib.pyplot as plt
from financial_engine import FinancialTimeMachine
from ai_advisor import AIFinancialAdvisor

def initialize_financial_data():
    """Initialize with sample financial data"""
    print("🔄 Initializing financial data...")
    ftm = FinancialTimeMachine(
        initial_balance=10000,
        current_income=6000,
        current_expenses=4500
    )
    
    # Sample transactions (past 6 months)
    transactions = [
        (6000, "salary", "2023-01-01"),
        (6000, "salary", "2023-02-01"),
        (6000, "salary", "2023-03-01"),
        (-2000, "rent", "2023-01-05"),
        (-1500, "rent", "2023-02-05"),
        (-2000, "rent", "2023-03-05"), 
        (-800, "groceries", "2023-01-10"),
        (-750, "groceries", "2023-02-10"),
        (-900, "groceries", "2023-03-10"),
        (-300, "utilities", "2023-01-15"),
        (-350, "utilities", "2023-02-15"),
        (-400, "utilities", "2023-03-15"),
        (-500, "entertainment", "2023-01-20"),
        (-600, "entertainment", "2023-02-20"),
        (-700, "entertainment", "2023-03-20")
    ]
    
    for amount, category, date in transactions:
        ftm.add_transaction(amount, category, date)
    
    return ftm

def setup_scenarios(ftm):
    """Configure financial scenarios"""
    print("\n🔄 Setting up scenarios...")
    scenarios = [
        ("Career Growth", 0.05, 0.02, 0.05),
        ("Frugal Living", 0.0, -0.15, 0.03),
        ("Aggressive Investing", 0.03, 0.0, 0.08)
    ]
    
    for name, income_change, expense_change, investment_return in scenarios:
        ftm.create_scenario(name, income_change, expense_change, investment_return)
        print(f"✅ Scenario: {name}")

def generate_visualizations(ftm):
    """Create and save financial projections"""
    print("\n📊 Generating visualizations...")
    try:
        projections = [
            ("Baseline", ftm.project_future(years=3)),
            ("Career Growth", ftm.project_future(years=3, scenario="Career Growth")),
            ("Frugal Living", ftm.project_future(years=3, scenario="Frugal Living"))
        ]
        
        for name, proj in projections:
            plt.figure(figsize=(10, 5))
            plt.plot(pd.to_datetime(proj['date']), proj['balance'], label='Balance')
            plt.plot(pd.to_datetime(proj['date']), proj['income'], label='Income')
            plt.plot(pd.to_datetime(proj['date']), proj['expenses'], label='Expenses')
            plt.title(f"Financial Projection: {name}")
            plt.xlabel('Date')
            plt.ylabel('Amount ($)')
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(f'{name.lower().replace(" ", "_")}_projection.png')
            print(f"✅ Saved: {name}_projection.png")
            
    except Exception as e:
        print(f"❌ Visualization error: {str(e)}", file=sys.stderr)

def main():
    print("\n" + "="*50)
    print("💰 FINANCIAL TIME MACHINE v1.0")
    print("="*50 + "\n")
    
    try:
        # 1. Initialize data
        ftm = initialize_financial_data()
        
        # 2. Setup scenarios
        setup_scenarios(ftm)
        
        # 3. Generate projections
        generate_visualizations(ftm)
        
        # 4. AI Recommendations
        print("\n🤖 AI Financial Advisor Analysis:")
        advisor = AIFinancialAdvisor(ftm)
        for i, recommendation in enumerate(advisor.suggest_optimizations(), 1):
            print(f"{i}. {recommendation}")
        
        # 5. Historical Analysis
        print("\n📅 Historical Performance:")
        history = ftm.analyze_past()
        for metric, value in history.items():
            print(f"- {metric.replace('_', ' ').title()}: ${value:,.2f}" 
                  if isinstance(value, (int, float)) 
                  else f"- {metric.replace('_', ' ').title()}: {value}")
    
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    # Additional imports (avoid circular imports)
    import pandas as pd
    import numpy as np
    
    try:
        main()
        print("\n" + "="*50)
        print("✅ Execution completed successfully!")
        print("="*50)
        
        # Keep window open on Windows
        if sys.platform == "win32":
            input("\nPress Enter to exit...")
            
    except KeyboardInterrupt:
        print("\n🚫 Operation cancelled by user")
        sys.exit(0)