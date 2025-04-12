from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
import numpy as np

class AIFinancialAdvisor:
    def __init__(self, financial_data):
        self.data = financial_data
    
    def suggest_optimizations(self):
        """Generate personalized financial recommendations"""
        if len(self.data.history) < 6:
            return ["Insufficient data for analysis. Please track at least 6 months of transactions."]
        
        # Analyze spending patterns
        spending_by_category = self.data.history.groupby('category')['expenses'].sum().sort_values(ascending=False)
        
        recommendations = []
        
        # High expense areas
        top_categories = spending_by_category.head(3).index.tolist()
        if top_categories:
            recommendations.append(
                f"Consider reducing spending on: {', '.join(top_categories)}"
            )
        
        # Savings potential
        savings_rate = self.data.analyze_past().get('savings_rate', 0)
        if savings_rate < 0.2:
            recommendations.append(
                f"Your savings rate is low ({savings_rate:.0%}). Aim to save at least 20% of income."
            )
        
        # Predict future cash flow
        try:
            X = np.arange(len(self.data.history)).reshape(-1, 1)
            y = self.data.history['balance'].values
            
            model = make_pipeline(
                PolynomialFeatures(degree=2),
                LinearRegression()
            )
            model.fit(X, y)
            
            future_months = 6
            prediction = model.predict([[len(self.data.history) + future_months]])[0]
            
            if prediction < 0:
                recommendations.append(
                    f"Projected negative balance in {future_months} months. Review expenses."
                )
        except:
            pass
        
        return recommendations if recommendations else ["Your finances appear healthy. Keep saving!"]