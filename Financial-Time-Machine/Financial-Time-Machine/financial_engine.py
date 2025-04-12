import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt

class FinancialTimeMachine:
    def __init__(self, initial_balance=0, current_income=0, current_expenses=0):
        self.current_finances = {
            'balance': initial_balance,
            'income': current_income,
            'expenses': current_expenses
        }
        self.history = pd.DataFrame(columns=['date', 'balance', 'income', 'expenses'])
        self.scenarios = {}
        self.goals = []
    
    def add_transaction(self, amount, category, date=None):
        """Record a financial transaction"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # Update balance
        self.current_finances['balance'] += amount
        if amount > 0:
            self.current_finances['income'] += amount
        else:
            self.current_finances['expenses'] += abs(amount)
        
        # Add to history
        new_row = pd.DataFrame([{
            'date': date,
            'balance': self.current_finances['balance'],
            'income': self.current_finances['income'],
            'expenses': self.current_finances['expenses'],
            'category': category
        }])
        self.history = pd.concat([self.history, new_row], ignore_index=True)
    
    def create_scenario(self, name, income_change=0, expense_change=0, investment_return=0):
        """Create a what-if financial scenario"""
        self.scenarios[name] = {
            'income_change': income_change,
            'expense_change': expense_change,
            'investment_return': investment_return
        }
    
    def project_future(self, years=5, scenario=None):
        """Project finances into the future"""
        projections = []
        current_date = datetime.now()
        
        # Get baseline or scenario parameters
        if scenario and scenario in self.scenarios:
            params = self.scenarios[scenario]
        else:
            params = {'income_change': 0, 'expense_change': 0, 'investment_return': 0}
        
        # Initialize projection
        projection = {
            'balance': self.current_finances['balance'],
            'income': self.current_finances['income'],
            'expenses': self.current_finances['expenses']
        }
        
        for month in range(years * 12):
            current_date += relativedelta(months=1)
            
            # Calculate new values
            new_income = projection['income'] * (1 + params['income_change']/12)
            new_expenses = projection['expenses'] * (1 + params['expense_change']/12)
            investment_growth = projection['balance'] * (params['investment_return']/12)
            
            projection['balance'] += (new_income - new_expenses + investment_growth)
            projection['income'] = new_income
            projection['expenses'] = new_expenses
            
            projections.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'balance': projection['balance'],
                'income': new_income,
                'expenses': new_expenses
            })
        
        return pd.DataFrame(projections)
    
    def visualize_projection(self, projections, title="Financial Projection"):
        """Create visualization of financial projections"""
        plt.figure(figsize=(12, 6))
        plt.plot(pd.to_datetime(projections['date']), projections['balance'], label='Balance')
        plt.plot(pd.to_datetime(projections['date']), projections['income'], label='Income')
        plt.plot(pd.to_datetime(projections['date']), projections['expenses'], label='Expenses')
        plt.title(title)
        plt.xlabel('Date')
        plt.ylabel('Amount ($)')
        plt.legend()
        plt.grid(True)
        plt.show()
    
    def analyze_past(self, lookback_years=5):
        """Analyze past financial performance"""
        if self.history.empty:
            return "No historical data available"
        
        # Convert dates and filter
        self.history['date'] = pd.to_datetime(self.history['date'])
        cutoff_date = datetime.now() - relativedelta(years=lookback_years)
        past_data = self.history[self.history['date'] >= cutoff_date]
        
        # Calculate metrics
        analysis = {
            'net_worth_change': past_data['balance'].iloc[-1] - past_data['balance'].iloc[0],
            'avg_monthly_income': past_data[past_data['income'] > 0]['income'].mean(),
            'avg_monthly_expenses': past_data[past_data['expenses'] > 0]['expenses'].mean(),
            'savings_rate': (past_data['income'].sum() - past_data['expenses'].sum()) / past_data['income'].sum()
        }
        
        return analysis