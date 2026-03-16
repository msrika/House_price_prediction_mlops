"""
Configuration management module
"""
import os
import yaml
from pathlib import Path
from typing import Any, Dict


class Config:
    """Configuration manager for MLOps pipeline"""
    
    def __init__(self, config_path: str = "configs/config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Config file not found: {self.config_path}")
            return {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (supports nested keys with dot notation)"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_project_name(self) -> str:
        return self.config.get('project', {}).get('name', 'House Price Prediction')
    
    def get_model_path(self) -> str:
        return self.config.get('model', {}).get('save_path', 'models/')
    
    def get_data_paths(self) -> Dict[str, str]:
        data_config = self.config.get('data', {})
        return {
            'raw': data_config.get('raw_path', 'data/raw/house_price.csv'),
            'processed': data_config.get('processed_path', 'data/processed/'),
            'test_size': data_config.get('test_size', 0.2),
            'random_state': data_config.get('random_state', 42)
        }
    
    def get_training_params(self) -> Dict[str, Any]:
        return self.config.get('training', {})
    
    def get_monitoring_config(self) -> Dict[str, Any]:
        return self.config.get('monitoring', {})


# Global config instance
config = Config()
