"""
Model monitoring and logging module
"""
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List
import pandas as pd
import numpy as np

from .config import config


class MonitoringLogger:
    """Monitor model predictions and performance"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.logger = logging.getLogger("MLOps_Monitor")
        self.logger.setLevel(logging.INFO)
        
        # Create handlers
        file_handler = logging.FileHandler(self.log_dir / "monitoring.log")
        console_handler = logging.StreamHandler()
        
        # Formatters
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        self.predictions_log = []
        self.performance_log = []
    
    def log_prediction(
        self,
        input_data: Dict,
        prediction: float,
        confidence: Optional[float] = None
    ):
        """Log individual prediction"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'input': input_data,
            'prediction': prediction,
            'confidence': confidence
        }
        
        self.predictions_log.append(log_entry)
        self.logger.info(f"Prediction: {prediction:.2f}")
        
        return log_entry
    
    def log_performance(
        self,
        metrics: Dict[str, float],
        batch_id: Optional[str] = None
    ):
        """Log model performance metrics"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'batch_id': batch_id or datetime.now().strftime("%Y%m%d"),
            'metrics': metrics
        }
        
        self.performance_log.append(log_entry)
        
        self.logger.info(f"Performance Metrics:")
        for metric, value in metrics.items():
            self.logger.info(f"  {metric}: {value:.4f}")
        
        return log_entry
    
    def log_drift_alert(self, drift_score: float, features: List[str]):
        """Log drift detection alert"""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'type': 'DATA_DRIFT',
            'severity': 'HIGH' if drift_score > 0.2 else 'MEDIUM',
            'drift_score': drift_score,
            'affected_features': features
        }
        
        self.logger.warning(f"🚨 Drift Alert: Score={drift_score:.4f}, Features={features}")
        
        return alert
    
    def log_model_degradation(
        self,
        current_metric: float,
        baseline_metric: float,
        metric_name: str
    ):
        """Log model performance degradation"""
        degradation_pct = ((baseline_metric - current_metric) / baseline_metric) * 100
        
        alert = {
            'timestamp': datetime.now().isoformat(),
            'type': 'MODEL_DEGRADATION',
            'metric': metric_name,
            'current_value': current_metric,
            'baseline_value': baseline_metric,
            'degradation_percentage': degradation_pct
        }
        
        severity = 'CRITICAL' if degradation_pct > 20 else 'WARNING'
        self.logger.warning(
            f"⚠️ {severity}: {metric_name} degraded from {baseline_metric:.4f} to {current_metric:.4f} "
            f"({degradation_pct:.2f}%)"
        )
        
        return alert
    
    def save_logs(self):
        """Save logs to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save predictions log
        if self.predictions_log:
            pred_file = self.log_dir / f"predictions_{timestamp}.json"
            with open(pred_file, 'w') as f:
                json.dump(self.predictions_log, f, indent=2)
            self.logger.info(f"Saved predictions log to {pred_file}")
        
        # Save performance log
        if self.performance_log:
            perf_file = self.log_dir / f"performance_{timestamp}.json"
            with open(perf_file, 'w') as f:
                json.dump(self.performance_log, f, indent=2)
            self.logger.info(f"Saved performance log to {perf_file}")
    
    def get_prediction_summary(self) -> pd.DataFrame:
        """Get summary of logged predictions"""
        if not self.predictions_log:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.predictions_log)
        return df


class PerformanceMonitor:
    """Monitor model performance over time"""
    
    def __init__(self, threshold: float = 0.8):
        self.threshold = threshold
        self.baseline_metrics = None
        self.alerts = []
    
    def set_baseline(self, metrics: Dict[str, float]):
        """Set baseline performance metrics"""
        self.baseline_metrics = metrics
        print(f"✓ Baseline metrics set: {metrics}")
    
    def check_performance(
        self,
        current_metrics: Dict[str, float]
    ) -> Dict:
        """Check if current performance meets threshold"""
        if self.baseline_metrics is None:
            raise ValueError("No baseline metrics set")
        
        results = {
            'passed': True,
            'violations': [],
            'details': {}
        }
        
        for metric_name, current_value in current_metrics.items():
            if metric_name not in self.baseline_metrics:
                continue
            
            baseline_value = self.baseline_metrics[metric_name]
            
            # For R² and similar metrics, higher is better
            if metric_name in ['r2', 'accuracy']:
                passed = current_value >= (baseline_value * self.threshold)
            # For error metrics, lower is better
            elif metric_name in ['mae', 'mse', 'rmse']:
                passed = current_value <= (baseline_value * (2 - self.threshold))
            else:
                passed = True
            
            results['details'][metric_name] = {
                'baseline': baseline_value,
                'current': current_value,
                'passed': passed
            }
            
            if not passed:
                results['violations'].append(metric_name)
                results['passed'] = False
        
        return results
    
    def add_alert(self, alert_type: str, message: str, severity: str = "WARNING"):
        """Add performance alert"""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'type': alert_type,
            'severity': severity,
            'message': message
        }
        
        self.alerts.append(alert)
        return alert
    
    def get_alerts(self) -> List[Dict]:
        """Get all alerts"""
        return self.alerts
