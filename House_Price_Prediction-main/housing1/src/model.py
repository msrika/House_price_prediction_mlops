"""
Model training and evaluation module
"""
import pickle
import joblib
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

from .config import config


class ModelTrainer:
    """Handle model training"""
    
    def __init__(self, model_type: str = "linear_regression"):
        self.model_type = model_type
        self.model = None
        self.training_params = config.get_training_params()
    
    def create_model(self):
        """Create model based on configuration"""
        if self.model_type == "linear_regression":
            self.model = LinearRegression(
                max_iter=self.training_params.get('max_iter', 1000)
            )
        elif self.model_type == "random_forest":
            self.model = RandomForestRegressor(
                n_estimators=100,
                random_state=42,
                n_jobs=-1
            )
        elif self.model_type == "gradient_boosting":
            self.model = GradientBoostingRegressor(
                random_state=42
            )
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
        
        print(f"✓ Created {self.model_type} model")
        return self.model
    
    def train(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series
    ):
        """Train the model"""
        if self.model is None:
            self.create_model()
        
        print("🚀 Training model...")
        self.model.fit(X_train, y_train)
        print("✓ Model training completed")
        
        return self.model
    
    def save_model(self, model_path: Optional[str] = None, model_name: Optional[str] = None):
        """Save trained model to disk"""
        if self.model is None:
            raise ValueError("No model to save. Train a model first.")
        
        model_path = model_path or config.get_model_path()
        model_name = model_name or f"{config.config['model']['name']}.pkl"
        
        Path(model_path).mkdir(parents=True, exist_ok=True)
        full_path = Path(model_path) / model_name
        
        # Save using joblib (better for large numpy arrays)
        joblib.dump(self.model, full_path)
        
        print(f"✓ Model saved to {full_path}")
        return full_path
    
    def load_model(self, model_path: str):
        """Load model from disk"""
        path = Path(model_path)
        if not path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        self.model = joblib.load(path)
        print(f"✓ Model loaded from {model_path}")
        return self.model


class ModelEvaluator:
    """Handle model evaluation and metrics"""
    
    def __init__(self):
        self.metrics = {}
    
    def evaluate(
        self,
        model,
        X_test: pd.DataFrame,
        y_test: pd.Series
    ) -> Dict[str, float]:
        """Evaluate model and compute metrics"""
        predictions = model.predict(X_test)
        
        self.metrics = {
            'mae': mean_absolute_error(y_test, predictions),
            'mse': mean_squared_error(y_test, predictions),
            'rmse': np.sqrt(mean_squared_error(y_test, predictions)),
            'r2': r2_score(y_test, predictions)
        }
        
        print("\n📊 Model Evaluation Metrics:")
        print(f"  Mean Absolute Error (MAE): {self.metrics['mae']:.2f}")
        print(f"  Mean Squared Error (MSE): {self.metrics['mse']:.2f}")
        print(f"  Root Mean Squared Error (RMSE): {self.metrics['rmse']:.2f}")
        print(f"  R² Score: {self.metrics['r2']:.4f}")
        
        return self.metrics
    
    def get_predictions(
        self,
        model,
        X: pd.DataFrame
    ) -> np.ndarray:
        """Get model predictions"""
        return model.predict(X)
    
    def compare_models(
        self,
        models: Dict[str, Any],
        X_test: pd.DataFrame,
        y_test: pd.Series
    ) -> pd.DataFrame:
        """Compare multiple models"""
        results = []
        
        for name, model in models.items():
            metrics = self.evaluate(model, X_test, y_test)
            results.append({
                'model': name,
                **metrics
            })
        
        return pd.DataFrame(results)
    
    def save_metrics(self, metrics: Dict[str, float], output_path: str):
        """Save evaluation metrics to file"""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            for metric, value in metrics.items():
                f.write(f"{metric}: {value}\n")
        
        print(f"✓ Metrics saved to {output_path}")
