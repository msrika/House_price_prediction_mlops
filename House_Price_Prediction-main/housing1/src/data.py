"""
Data loading and preprocessing module
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Optional
from sklearn.model_selection import train_test_split

from .config import config


class DataLoader:
    """Handle data loading and basic validation"""
    
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path or config.get('data.raw_path')
        self.data: Optional[pd.DataFrame] = None
    
    def load_data(self) -> pd.DataFrame:
        """Load data from CSV file"""
        try:
            self.data = pd.read_csv(self.file_path)
            print(f"✓ Loaded data from {self.file_path}")
            print(f"  Shape: {self.data.shape}")
            return self.data
        except FileNotFoundError:
            raise FileNotFoundError(f"Data file not found: {self.file_path}")
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")
    
    def get_data_summary(self) -> dict:
        """Get summary statistics of the data"""
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        return {
            'shape': self.data.shape,
            'columns': list(self.data.columns),
            'missing_values': self.data.isnull().sum().to_dict(),
            'dtypes': self.data.dtypes.astype(str).to_dict()
        }


class DataPreprocessor:
    """Handle data preprocessing and splitting"""
    
    def __init__(self):
        self.data_config = config.get_data_paths()
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
    
    def prepare_features(
        self, 
        df: pd.DataFrame, 
        target_column: str
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """Separate features and target"""
        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found in dataframe")
        
        X = df.drop(target_column, axis=1)
        y = df[target_column]
        
        return X, y
    
    def split_data(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        test_size: Optional[float] = None,
        random_state: Optional[int] = None
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """Split data into training and testing sets"""
        test_size = test_size or self.data_config['test_size']
        random_state = random_state or self.data_config['random_state']
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        print(f"✓ Data split successfully")
        print(f"  Training set: {len(self.X_train)} samples")
        print(f"  Test set: {len(self.X_test)} samples")
        
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def save_processed_data(
        self,
        X_train: pd.DataFrame,
        X_test: pd.DataFrame,
        y_train: pd.Series,
        y_test: pd.Series
    ):
        """Save processed data for reproducibility"""
        output_dir = Path(self.data_config['processed'])
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Combine features and target for saving
        train_data = pd.concat([X_train, y_train], axis=1)
        test_data = pd.concat([X_test, y_test], axis=1)
        
        train_data.to_csv(output_dir / "train.csv", index=False)
        test_data.to_csv(output_dir / "test.csv", index=False)
        
        print(f"✓ Saved processed data to {output_dir}")
