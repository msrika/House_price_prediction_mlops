"""
Visualization module for House Price Prediction app
Creates charts and graphs for data exploration and model insights
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import io
import base64
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

class DataVisualizer:
    """Class to handle data visualization for the house price prediction app"""
    
    def __init__(self, data_path=None):
        if data_path is None:
            import os
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(BASE_DIR, "Data", "house_price.csv")
        self.data_path = data_path
        self.df = None
        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.y_pred = None
        
    def load_data(self):
        """Load the house price data"""
        try:
            self.df = pd.read_csv(self.data_path)
            print(f"Data loaded successfully. Shape: {self.df.shape}")
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def create_correlation_heatmap(self, figsize=(10, 8)):
        """Create correlation heatmap of features"""
        if self.df is None:
            self.load_data()
        
        plt.figure(figsize=figsize)
        correlation_matrix = self.df.corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
                    square=True, fmt='.2f')
        plt.title('Correlation Heatmap of House Features')
        plt.tight_layout()
        
        # Save to bytes
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return img_str
    
    def create_feature_distributions(self, figsize=(15, 10)):
        """Create distribution plots for all features"""
        if self.df is None:
            self.load_data()
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        n_cols = 3
        n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
        axes = axes.flatten() if n_rows > 1 else [axes] if len(numeric_cols) == 1 else axes
        
        for i, col in enumerate(numeric_cols):
            if i < len(axes):
                axes[i].hist(self.df[col], bins=20, edgecolor='black', alpha=0.7)
                axes[i].set_title(f'Distribution of {col}')
                axes[i].set_xlabel(col)
                axes[i].set_ylabel('Frequency')
        
        # Hide unused subplots
        for i in range(len(numeric_cols), len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        
        # Save to bytes
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return img_str
    
    def create_scatter_plots(self, figsize=(15, 10)):
        """Create scatter plots of features vs price"""
        if self.df is None:
            self.load_data()
        
        # Identify features (all columns except 'Price')
        feature_cols = [col for col in self.df.columns if col != 'Price']
        
        n_cols = 3
        n_rows = (len(feature_cols) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
        if len(feature_cols) == 1:
            axes = [axes]
        else:
            axes = axes.flatten() if n_rows > 1 else axes
        
        for i, col in enumerate(feature_cols):
            if i < len(axes):
                axes[i].scatter(self.df[col], self.df['Price'], alpha=0.6)
                axes[i].set_xlabel(col)
                axes[i].set_ylabel('Price')
                axes[i].set_title(f'{col} vs Price')
                
                # Add trend line
                z = np.polyfit(self.df[col], self.df['Price'], 1)
                p = np.poly1d(z)
                axes[i].plot(self.df[col], p(self.df[col]), "r--", alpha=0.8)
        
        # Hide unused subplots
        for i in range(len(feature_cols), len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        
        # Save to bytes
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return img_str
    
    def create_model_performance_charts(self, model_type='linear'):
        """Create model performance visualization"""
        if self.df is None:
            self.load_data()
        
        # Prepare data
        X = self.df.drop('Price', axis=1)
        y = self.df['Price']
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model based on type
        if model_type == 'linear':
            self.model = LinearRegression()
        elif model_type == 'random_forest':
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        
        self.model.fit(self.X_train, self.y_train)
        
        # Make predictions
        self.y_pred = self.model.predict(self.X_test)
        
        # Calculate metrics
        r2 = r2_score(self.y_test, self.y_pred)
        mae = mean_absolute_error(self.y_test, self.y_pred)
        mse = mean_squared_error(self.y_test, self.y_pred)
        rmse = np.sqrt(mse)
        
        # Create subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Actual vs Predicted
        axes[0, 0].scatter(self.y_test, self.y_pred, alpha=0.6)
        axes[0, 0].plot([self.y_test.min(), self.y_test.max()], 
                        [self.y_test.min(), self.y_test.max()], 'r--', lw=2)
        axes[0, 0].set_xlabel('Actual Price')
        axes[0, 0].set_ylabel('Predicted Price')
        axes[0, 0].set_title(f'Actual vs Predicted Prices\n(R² = {r2:.3f})')
        
        # 2. Residuals plot
        residuals = self.y_test - self.y_pred
        axes[0, 1].scatter(self.y_pred, residuals, alpha=0.6)
        axes[0, 1].axhline(y=0, color='r', linestyle='--')
        axes[0, 1].set_xlabel('Predicted Price')
        axes[0, 1].set_ylabel('Residuals')
        axes[0, 1].set_title('Residual Plot')
        
        # 3. Feature importance (coefficients for linear, feature importance for RF)
        if model_type == 'linear':
            feature_importance = np.abs(self.model.coef_)
            feature_names = X.columns
        else:
            feature_importance = self.model.feature_importances_
            feature_names = X.columns
            
        indices = np.argsort(feature_importance)[::-1]
        
        axes[1, 0].bar(range(len(feature_importance)), feature_importance[indices])
        axes[1, 0].set_xlabel('Features')
        axes[1, 0].set_ylabel('Importance')
        axes[1, 0].set_title('Feature Importance')
        axes[1, 0].set_xticks(range(len(feature_importance)))
        axes[1, 0].set_xticklabels([feature_names[i] for i in indices], rotation=45)
        
        # 4. Model metrics
        metrics = ['R²', 'MAE', 'RMSE']
        values = [r2, mae, rmse]
        bars = axes[1, 1].bar(metrics, values, color=['blue', 'orange', 'green'])
        axes[1, 1].set_ylabel('Value')
        axes[1, 1].set_title('Model Performance Metrics')
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            axes[1, 1].text(bar.get_x() + bar.get_width()/2., height,
                            f'{value:.2f}',
                            ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Save to bytes
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return img_str, {'r2': r2, 'mae': mae, 'mse': mse, 'rmse': rmse}
    
    def create_interactive_dashboard(self):
        """Create an interactive dashboard using Plotly"""
        if self.df is None:
            self.load_data()
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Price Distribution', 'Area vs Price', 
                          'Bedrooms vs Price', 'Correlation Heatmap'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # 1. Price Distribution
        fig.add_trace(
            go.Histogram(x=self.df['Price'], name='Price Distribution'),
            row=1, col=1
        )
        
        # 2. Area vs Price
        fig.add_trace(
            go.Scatter(x=self.df['Area'], y=self.df['Price'], 
                      mode='markers', name='Area vs Price',
                      marker=dict(size=8, opacity=0.6)),
            row=1, col=2
        )
        
        # 3. Bedrooms vs Price
        fig.add_trace(
            go.Box(x=self.df['Bedrooms'], y=self.df['Price'], 
                   name='Bedrooms vs Price'),
            row=2, col=1
        )
        
        # 4. Correlation heatmap
        corr_matrix = self.df.select_dtypes(include=[np.number]).corr()
        fig.add_trace(
            go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                name='Correlation',
                showscale=True
            ),
            row=2, col=2
        )
        
        fig.update_layout(height=800, showlegend=False, 
                         title_text="Interactive Data Dashboard")
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def get_data_insights(self):
        """Generate data insights and statistics"""
        if self.df is None:
            self.load_data()
        
        insights = {
            'basic_stats': self.df.describe().to_dict(),
            'shape': self.df.shape,
            'columns': list(self.df.columns),
            'missing_values': self.df.isnull().sum().to_dict(),
            'numeric_columns': list(self.df.select_dtypes(include=[np.number]).columns),
            'categorical_columns': list(self.df.select_dtypes(exclude=[np.number]).columns),
            'price_stats': {
                'mean': float(self.df['Price'].mean()),
                'median': float(self.df['Price'].median()),
                'std': float(self.df['Price'].std()),
                'min': float(self.df['Price'].min()),
                'max': float(self.df['Price'].max())
            }
        }
        
        return insights

# Example usage function
def create_sample_visualizations():
    """Function to create sample visualizations for demonstration"""
    viz = DataVisualizer()
    if viz.load_data():
        print("Creating sample visualizations...")
        
        # Create correlation heatmap
        corr_img = viz.create_correlation_heatmap()
        print(f"Correlation heatmap created: {len(corr_img)} characters")
        
        # Create feature distributions
        dist_img = viz.create_feature_distributions()
        print(f"Distribution plots created: {len(dist_img)} characters")
        
        # Create scatter plots
        scatter_img = viz.create_scatter_plots()
        print(f"Scatter plots created: {len(scatter_img)} characters")
        
        # Create model performance charts
        perf_img, metrics = viz.create_model_performance_charts()
        print(f"Performance charts created: {len(perf_img)} characters")
        print(f"Model metrics: {metrics}")
        
        return True
    else:
        print("Failed to load data for visualization")
        return False

if __name__ == "__main__":
    create_sample_visualizations()