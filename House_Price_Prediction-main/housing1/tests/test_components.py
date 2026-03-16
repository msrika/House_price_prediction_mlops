"""
Unit tests for MLOps components
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import Config
from src.data import DataLoader, DataPreprocessor
from src.model import ModelTrainer, ModelEvaluator
from src.validation import DataValidator, DriftDetector


class TestConfig:
    """Test configuration management"""
    
    def test_config_loads(self):
        """Test that config loads successfully"""
        config = Config("configs/config.yaml")
        assert config.config is not None
    
    def test_config_get_nested_value(self):
        """Test getting nested config values"""
        config = Config("configs/config.yaml")
        project_name = config.get('project.name')
        assert project_name is not None
    
    def test_config_get_data_paths(self):
        """Test getting data paths"""
        config = Config("configs/config.yaml")
        data_paths = config.get_data_paths()
        assert 'raw' in data_paths
        assert 'processed' in data_paths


class TestDataLoader:
    """Test data loading functionality"""
    
    def test_data_loader_initialization(self):
        """Test data loader initializes"""
        loader = DataLoader()
        assert loader is not None
    
    def test_data_loader_summary(self):
        """Test data summary generation"""
        # Create sample data
        df = pd.DataFrame({
            'Area': [1000, 2000, 3000],
            'Price': [100000, 200000, 300000]
        })
        
        loader = DataLoader()
        loader.data = df
        
        summary = loader.get_data_summary()
        assert summary['shape'] == (3, 2)
        assert 'Area' in summary['columns']


class TestDataPreprocessor:
    """Test data preprocessing"""
    
    def test_prepare_features(self):
        """Test feature preparation"""
        df = pd.DataFrame({
            'Area': [1000, 2000, 3000],
            'Bedrooms': [2, 3, 4],
            'Price': [100000, 200000, 300000]
        })
        
        preprocessor = DataPreprocessor()
        X, y = preprocessor.prepare_features(df, 'Price')
        
        assert 'Price' not in X.columns
        assert len(y) == 3
    
    def test_split_data(self):
        """Test data splitting"""
        df = pd.DataFrame({
            'Area': list(range(100)),
            'Price': list(range(100, 200))
        })
        
        preprocessor = DataPreprocessor()
        X, y = preprocessor.prepare_features(df, 'Price')
        X_train, X_test, y_train, y_test = preprocessor.split_data(X, y)
        
        assert len(X_train) > 0
        assert len(X_test) > 0
        assert len(X_train) + len(X_test) == len(X)


class TestModelTrainer:
    """Test model training"""
    
    def test_model_creation(self):
        """Test model creation"""
        trainer = ModelTrainer("linear_regression")
        model = trainer.create_model()
        assert model is not None
    
    def test_model_training(self):
        """Test model training"""
        X_train = pd.DataFrame({
            'Area': [1000, 2000, 3000, 4000, 5000],
            'Bedrooms': [2, 3, 4, 5, 6]
        })
        y_train = pd.Series([100000, 200000, 300000, 400000, 500000])
        
        trainer = ModelTrainer("linear_regression")
        model = trainer.train(X_train, y_train)
        
        assert model is not None
    
    def test_model_prediction(self):
        """Test model prediction"""
        X_train = pd.DataFrame({
            'Area': [1000, 2000, 3000, 4000, 5000],
            'Bedrooms': [2, 3, 4, 5, 6]
        })
        y_train = pd.Series([100000, 200000, 300000, 400000, 500000])
        
        trainer = ModelTrainer("linear_regression")
        trainer.train(X_train, y_train)
        
        X_test = pd.DataFrame({'Area': [2500], 'Bedrooms': [3]})
        prediction = trainer.model.predict(X_test)[0]
        
        assert prediction > 0


class TestModelEvaluator:
    """Test model evaluation"""
    
    def test_evaluation_metrics(self):
        """Test evaluation metrics calculation"""
        y_true = pd.Series([100, 200, 300, 400, 500])
        y_pred = np.array([110, 190, 310, 390, 510])
        
        evaluator = ModelEvaluator()
        model = type('MockModel', (), {'predict': lambda self, X: y_pred})()
        
        X_test = pd.DataFrame({'Area': [1000, 2000, 3000, 4000, 5000]})
        metrics = evaluator.evaluate(model, X_test, y_true)
        
        assert 'mae' in metrics
        assert 'mse' in metrics
        assert 'rmse' in metrics
        assert 'r2' in metrics


class TestDataValidator:
    """Test data validation"""
    
    def test_data_quality_check(self):
        """Test data quality validation"""
        df = pd.DataFrame({
            'Area': [1000, 2000, 3000, 4000, 5000],
            'Price': [100000, 200000, 300000, 400000, 500000]
        })
        
        validator = DataValidator()
        report = validator.validate_data_quality(df)
        
        assert 'quality_score' in report
        assert report['quality_score'] == 100.0  # Perfect data
    
    def test_missing_values_detection(self):
        """Test missing value detection"""
        df = pd.DataFrame({
            'Area': [1000, np.nan, 3000, 4000, 5000],
            'Price': [100000, 200000, 300000, 400000, 500000]
        })
        
        validator = DataValidator()
        report = validator.validate_data_quality(df)
        
        assert 'missing_values' in report
        assert len(report['missing_values']) > 0


class TestDriftDetector:
    """Test drift detection"""
    
    def test_drift_detection(self):
        """Test basic drift detection"""
        reference = pd.DataFrame({
            'Area': np.random.normal(2000, 500, 1000)
        })
        
        current = pd.DataFrame({
            'Area': np.random.normal(2000, 500, 1000)
        })
        
        detector = DriftDetector()
        detector.fit(reference)
        results = detector.detect_drift(current)
        
        assert 'drift_detected' in results
        assert 'drift_scores' in results


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
