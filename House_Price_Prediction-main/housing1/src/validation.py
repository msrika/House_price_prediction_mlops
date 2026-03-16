"""
Data validation and drift detection module
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from scipy import stats
from sklearn.preprocessing import StandardScaler

from .config import config


class DataValidator:
    """Validate data quality and schema"""
    
    def __init__(self):
        self.schema = None
        self.validation_results = {}
    
    def define_schema(self, expected_columns: List[str], expected_dtypes: Dict[str, str]):
        """Define expected data schema"""
        self.schema = {
            'columns': expected_columns,
            'dtypes': expected_dtypes
        }
    
    def validate_schema(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """Validate dataframe schema"""
        issues = []
        
        # Check columns
        if self.schema and 'columns' in self.schema:
            missing_cols = set(self.schema['columns']) - set(df.columns)
            if missing_cols:
                issues.append(f"Missing columns: {missing_cols}")
        
        # Check data types
        if self.schema and 'dtypes' in self.schema:
            for col, expected_dtype in self.schema['dtypes'].items():
                if col in df.columns:
                    actual_dtype = str(df[col].dtype)
                    if expected_dtype not in actual_dtype.lower():
                        issues.append(
                            f"Column '{col}' has dtype {actual_dtype}, expected {expected_dtype}"
                        )
        
        is_valid = len(issues) == 0
        return is_valid, issues
    
    def validate_data_quality(self, df: pd.DataFrame) -> Dict:
        """Comprehensive data quality check"""
        quality_report = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'missing_values': {},
            'duplicate_rows': df.duplicated().sum(),
            'outliers': {},
            'quality_score': 100.0
        }
        
        # Check missing values
        for col in df.columns:
            missing_count = df[col].isnull().sum()
            missing_pct = (missing_count / len(df)) * 100
            
            if missing_count > 0:
                quality_report['missing_values'][col] = {
                    'count': missing_count,
                    'percentage': round(missing_pct, 2)
                }
        
        # Check for outliers (using IQR method)
        for col in df.select_dtypes(include=[np.number]).columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
            
            if outliers > 0:
                quality_report['outliers'][col] = {
                    'count': int(outliers),
                    'percentage': round((outliers / len(df)) * 100, 2)
                }
        
        # Calculate quality score
        penalty = 0
        penalty += sum(v['percentage'] for v in quality_report['missing_values'].values())
        penalty += sum(v['percentage'] for v in quality_report['outliers'].values())
        penalty += (quality_report['duplicate_rows'] / len(df)) * 100
        
        quality_report['quality_score'] = max(0, 100 - penalty)
        
        self.validation_results = quality_report
        return quality_report
    
    def print_validation_report(self):
        """Print validation report"""
        if not self.validation_results:
            print("No validation results available")
            return
        
        print("\n📋 Data Validation Report:")
        print(f"  Total Rows: {self.validation_results['total_rows']}")
        print(f"  Total Columns: {self.validation_results['total_columns']}")
        print(f"  Duplicate Rows: {self.validation_results['duplicate_rows']}")
        print(f"  Quality Score: {self.validation_results['quality_score']:.2f}%")
        
        if self.validation_results['missing_values']:
            print("\n  Missing Values:")
            for col, info in self.validation_results['missing_values'].items():
                print(f"    {col}: {info['count']} ({info['percentage']}%)")
        
        if self.validation_results['outliers']:
            print("\n  Outliers:")
            for col, info in self.validation_results['outliers'].items():
                print(f"    {col}: {info['count']} ({info['percentage']}%)")


class DriftDetector:
    """Detect data drift between reference and current data"""
    
    def __init__(self, threshold: float = 0.1):
        self.threshold = threshold
        self.reference_stats = None
        self.drift_results = {}
    
    def fit(self, reference_data: pd.DataFrame):
        """Set reference data statistics"""
        self.reference_stats = {
            'mean': reference_data.mean(),
            'std': reference_data.std(),
            'median': reference_data.median(),
            'distribution': reference_data
        }
        
        print("✓ Reference data statistics computed")
    
    def detect_drift(
        self, 
        current_data: pd.DataFrame,
        method: str = "ks_test"
    ) -> Dict:
        """Detect drift between reference and current data"""
        if self.reference_stats is None:
            raise ValueError("No reference data. Call fit() first.")
        
        drift_report = {
            'drift_detected': False,
            'features_with_drift': [],
            'drift_scores': {},
            'details': {}
        }
        
        numerical_cols = current_data.select_dtypes(include=[np.number]).columns
        
        for col in numerical_cols:
            if col not in self.reference_stats['mean'].index:
                continue
            
            ref_data = self.reference_stats['distribution'][col].dropna()
            curr_data = current_data[col].dropna()
            
            if method == "ks_test":
                # Kolmogorov-Smirnov test
                statistic, p_value = stats.ks_2samp(ref_data, curr_data)
                drift_score = statistic
                has_drift = p_value < self.threshold
                
            elif method == "psi":
                # Population Stability Index
                drift_score = self._calculate_psi(ref_data, curr_data)
                has_drift = drift_score > self.threshold
                
            else:
                # Simple mean shift
                mean_diff = abs(curr_data.mean() - ref_data.mean())
                std_diff = ref_data.std() if ref_data.std() > 0 else 1
                drift_score = mean_diff / std_diff
                has_drift = drift_score > self.threshold
            
            drift_report['drift_scores'][col] = drift_score
            drift_report['details'][col] = {
                'reference_mean': float(ref_data.mean()),
                'current_mean': float(curr_data.mean()),
                'drift_score': float(drift_score),
                'has_drift': bool(has_drift)
            }
            
            if has_drift:
                drift_report['features_with_drift'].append(col)
                drift_report['drift_detected'] = True
        
        self.drift_results = drift_report
        return drift_report
    
    def _calculate_psi(
        self, 
        reference: pd.Series, 
        current: pd.Series,
        buckets: int = 10
    ) -> float:
        """Calculate Population Stability Index"""
        # Create buckets based on reference data
        percentiles = np.linspace(0, 100, buckets + 1)
        breakpoints = np.percentile(reference, percentiles)
        breakpoints[-1] += 0.001  # Include max value
        
        # Count observations in each bucket
        ref_counts = np.histogram(reference, bins=breakpoints)[0]
        curr_counts = np.histogram(current, bins=breakpoints)[0]
        
        # Calculate percentages
        ref_perc = (ref_counts + 0.0001) / len(reference)
        curr_perc = (curr_counts + 0.0001) / len(current)
        
        # Calculate PSI
        psi = np.sum((curr_perc - ref_perc) * np.log(curr_perc / ref_perc))
        
        return psi
    
    def print_drift_report(self):
        """Print drift detection report"""
        if not self.drift_results:
            print("No drift results available")
            return
        
        print("\n🔍 Drift Detection Report:")
        print(f"  Drift Detected: {'Yes ⚠️' if self.drift_results['drift_detected'] else 'No ✓'}")
        
        if self.drift_results['features_with_drift']:
            print(f"\n  Features with drift ({len(self.drift_results['features_with_drift'])}):")
            for feature in self.drift_results['features_with_drift']:
                details = self.drift_results['details'][feature]
                print(f"    {feature}:")
                print(f"      Reference Mean: {details['reference_mean']:.2f}")
                print(f"      Current Mean: {details['current_mean']:.2f}")
                print(f"      Drift Score: {details['drift_score']:.4f}")
