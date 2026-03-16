"""
Experiment tracking and model registry module
"""
import json
import pickle
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
import pandas as pd

from .config import config


class ExperimentTracker:
    """Track experiments and model performance"""
    
    def __init__(self, experiment_name: Optional[str] = None):
        self.experiment_name = experiment_name or config.get('experiment.experiment_name', 'house_price_experiment')
        self.tracking_dir = Path("experiments") / self.experiment_name
        self.tracking_dir.mkdir(parents=True, exist_ok=True)
        
        self.current_run = None
        self.runs = []
    
    def start_run(self, run_name: Optional[str] = None) -> str:
        """Start a new experiment run"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_name = run_name or f"run_{timestamp}"
        
        self.current_run = {
            'run_id': f"{run_name}_{timestamp}",
            'run_name': run_name,
            'start_time': datetime.now().isoformat(),
            'parameters': {},
            'metrics': {},
            'artifacts': [],
            'status': 'running'
        }
        
        print(f"🚀 Starting experiment run: {run_name}")
        return self.current_run['run_id']
    
    def log_parameters(self, params: Dict[str, Any]):
        """Log training parameters"""
        if self.current_run:
            self.current_run['parameters'].update(params)
            print(f"✓ Logged parameters: {list(params.keys())}")
    
    def log_metrics(self, metrics: Dict[str, float]):
        """Log evaluation metrics"""
        if self.current_run:
            self.current_run['metrics'].update(metrics)
            print(f"✓ Logged metrics: {list(metrics.keys())}")
    
    def log_artifact(self, artifact_path: str):
        """Log an artifact (model file, plot, etc.)"""
        if self.current_run:
            self.current_run['artifacts'].append(artifact_path)
            print(f"✓ Logged artifact: {artifact_path}")
    
    def end_run(self, status: str = "completed"):
        """End the current run"""
        if self.current_run:
            self.current_run['end_time'] = datetime.now().isoformat()
            self.current_run['status'] = status
            
            # Save run to file
            self._save_run()
            
            self.runs.append(self.current_run)
            self.current_run = None
            
            print(f"✓ Run completed with status: {status}")
    
    def _save_run(self):
        """Save run data to JSON file"""
        run_file = self.tracking_dir / f"{self.current_run['run_id']}.json"
        
        with open(run_file, 'w') as f:
            json.dump(self.current_run, f, indent=2)
        
        print(f"✓ Run saved to {run_file}")
    
    def get_all_runs(self) -> List[Dict]:
        """Get all experiment runs"""
        runs = []
        
        for run_file in self.tracking_dir.glob("*.json"):
            with open(run_file, 'r') as f:
                runs.append(json.load(f))
        
        return runs
    
    def get_best_run(self, metric: str = 'r2', higher_is_better: bool = True) -> Optional[Dict]:
        """Get the best run based on a metric"""
        runs = self.get_all_runs()
        
        if not runs:
            return None
        
        # Filter completed runs
        completed_runs = [r for r in runs if r['status'] == 'completed']
        
        if not completed_runs:
            return None
        
        # Sort by metric
        if higher_is_better:
            best_run = max(completed_runs, key=lambda x: x['metrics'].get(metric, 0))
        else:
            best_run = min(completed_runs, key=lambda x: x['metrics'].get(metric, float('inf')))
        
        return best_run
    
    def compare_runs(self, metric: str = 'r2') -> pd.DataFrame:
        """Compare all runs"""
        runs = self.get_all_runs()
        
        data = []
        for run in runs:
            if run['status'] == 'completed':
                data.append({
                    'run_id': run['run_id'],
                    'run_name': run['run_name'],
                    metric: run['metrics'].get(metric, None),
                    'mae': run['metrics'].get('mae', None),
                    'rmse': run['metrics'].get('rmse', None),
                    'start_time': run['start_time']
                })
        
        return pd.DataFrame(data)


class ModelRegistry:
    """Registry for model versions"""
    
    def __init__(self):
        self.registry_dir = Path("models/registry")
        self.registry_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.registry_dir / "metadata.json"
        self.models = self._load_metadata()
    
    def _load_metadata(self) -> Dict:
        """Load model registry metadata"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return {"models": [], "latest_version": None}
    
    def register_model(
        self,
        model_path: str,
        version: str,
        metrics: Dict[str, float],
        description: str = ""
    ):
        """Register a new model version"""
        model_entry = {
            'version': version,
            'path': model_path,
            'metrics': metrics,
            'description': description,
            'registered_at': datetime.now().isoformat(),
            'status': 'active'
        }
        
        # Add to registry
        self.models['models'].append(model_entry)
        self.models['latest_version'] = version
        
        # Save metadata
        self._save_metadata()
        
        # Copy model to registry
        dest_path = self.registry_dir / f"model_v{version}.pkl"
        from shutil import copy2
        copy2(model_path, dest_path)
        
        print(f"✓ Registered model version {version}")
        print(f"  Path: {dest_path}")
        print(f"  Metrics: {metrics}")
        
        return model_entry
    
    def _save_metadata(self):
        """Save model registry metadata"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.models, f, indent=2)
    
    def get_model_version(self, version: str) -> Optional[Dict]:
        """Get model info by version"""
        for model in self.models['models']:
            if model['version'] == version:
                return model
        return None
    
    def get_latest_model(self) -> Optional[Dict]:
        """Get latest model version"""
        if self.models['latest_version']:
            return self.get_model_version(self.models['latest_version'])
        return None
    
    def list_models(self) -> pd.DataFrame:
        """List all registered models"""
        models_data = []
        
        for model in self.models['models']:
            models_data.append({
                'version': model['version'],
                'r2': model['metrics'].get('r2', None),
                'mae': model['metrics'].get('mae', None),
                'rmse': model['metrics'].get('rmse', None),
                'registered_at': model['registered_at'],
                'status': model['status']
            })
        
        return pd.DataFrame(models_data)
