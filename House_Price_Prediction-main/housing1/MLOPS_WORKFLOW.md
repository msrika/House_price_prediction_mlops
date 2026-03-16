# MLOps Workflow Guide

This document describes the complete MLOps workflow for the House Price Prediction project.

## 📋 Overview

```
Data Collection → Validation → Training → Evaluation → Registration → Deployment → Monitoring
```

## 1️⃣ Data Management

### Collect Data
```bash
# Place your CSV file in data/raw/
# Example: data/raw/house_price.csv
```

### Validate Data
```bash
# Validate data quality
python -c "from src.validation import DataValidator; \
from src.data import DataLoader; \
loader = DataLoader(); df = loader.load_data(); \
validator = DataValidator(); \
report = validator.validate_data_quality(df); \
validator.print_validation_report()"
```

### Data Quality Checks
- ✅ Missing values detection
- ✅ Outlier detection (IQR method)
- ✅ Duplicate detection
- ✅ Schema validation
- ✅ Quality score calculation

## 2️⃣ Model Training

### Train Model
```bash
# Using Makefile
make train

# Or directly
python pipelines/train.py --target Price
```

### Training Pipeline Steps
1. **Load Data** - Read from CSV
2. **Validate** - Check data quality
3. **Preprocess** - Split features and target
4. **Train** - Fit the model
5. **Evaluate** - Compute metrics
6. **Track** - Log to experiment tracker
7. **Save** - Persist model to disk
8. **Register** - Add to model registry

### Training Output
```
✓ Model saved to models/house_price_model.pkl
✓ R² Score: 0.85
✓ RMSE: 15000
```

## 3️⃣ Experiment Tracking

### Start Experiment
```python
from src.tracking import ExperimentTracker

tracker = ExperimentTracker()
run_id = tracker.start_run('my_experiment')
```

### Log Parameters
```python
tracker.log_parameters({
    'model_type': 'linear_regression',
    'test_size': 0.2,
    'max_iter': 1000
})
```

### Log Metrics
```python
tracker.log_metrics({
    'mae': 10000,
    'mse': 150000000,
    'rmse': 12247,
    'r2': 0.85
})
```

### End Experiment
```python
tracker.end_run(status='completed')
```

### View Experiments
```bash
# List all runs
make experiments

# Find best run
make best-experiment
```

## 4️⃣ Model Registry

### Register Model
```python
from src.tracking import ModelRegistry

registry = ModelRegistry()
registry.register_model(
    model_path='models/house_price_model.pkl',
    version='1.0.0',
    metrics={'r2': 0.85, 'mae': 10000},
    description='Production-ready model'
)
```

### List Models
```python
models = registry.list_models()
print(models)
```

### Get Latest Model
```python
latest = registry.get_latest_model()
print(f"Latest version: {latest['version']}")
```

## 5️⃣ Model Deployment

### Deploy to API
```bash
# Development
make api

# Production with gunicorn
make api-prod

# Docker
make docker-build
make docker-run
```

### API Endpoints
- `GET /` - Home page
- `POST /predict` - Form-based prediction
- `POST /api/v1/predict` - REST API
- `GET /health` - Health check
- `GET /metrics` - Model metrics

### Test Deployment
```bash
curl http://localhost:5000/health
curl -X POST http://localhost:5000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"Area": 2000, "Bedrooms": 3, ...}'
```

## 6️⃣ Monitoring

### Log Predictions
```python
from src.monitoring import MonitoringLogger

monitor = MonitoringLogger()
monitor.log_prediction(
    input_data={'Area': 2000, 'Bedrooms': 3},
    prediction=250000
)
```

### Log Performance
```python
monitor.log_performance({
    'mae': 10000,
    'rmse': 12247,
    'r2': 0.85
}, batch_id='daily_check')
```

### Detect Drift
```python
from src.validation import DriftDetector

detector = DriftDetector()
detector.fit(reference_data)
results = detector.detect_drift(current_data)
detector.print_drift_report()
```

### Performance Alerts
```python
from src.monitoring import PerformanceMonitor

perf_monitor = PerformanceMonitor(threshold=0.8)
perf_monitor.set_baseline({'r2': 0.85, 'mae': 10000})

results = perf_monitor.check_performance(current_metrics)
if not results['passed']:
    print(f"Performance degradation detected!")
```

## 7️⃣ CI/CD Pipeline

### Automated Workflows

#### On Push to Main
1. Run tests
2. Lint code
3. Type checking
4. Build Docker image
5. Validate model
6. Deploy to staging
7. Integration tests
8. Deploy to production

#### Manual Commands
```bash
# Run all CI checks
make ci

# Build for CD
make cd
```

## 8️⃣ Testing Strategy

### Unit Tests
```bash
# Run all tests
make test

# With coverage
make test-cov
```

### Test Components
- ✅ Configuration loading
- ✅ Data loading and preprocessing
- ✅ Model training
- ✅ Model evaluation
- ✅ Data validation
- ✅ Drift detection

### Integration Tests
```bash
# Test complete pipeline
python pipelines/train.py --target Price

# Test API
curl http://localhost:5000/health
```

## 9️⃣ Code Quality

### Linting
```bash
make lint
```

### Type Checking
```bash
make type-check
```

### Formatting
```bash
make format
```

### Pre-commit Hooks
```bash
# Install pre-commit
pip install pre-commit
pre-commit install

# Run manually
pre-commit run --all-files
```

## 🔟 Maintenance

### Regular Tasks

#### Daily
- Check monitoring logs
- Review prediction volume
- Check for drift alerts

#### Weekly
- Review model performance
- Analyze prediction accuracy
- Retrain if needed

#### Monthly
- Full model retraining
- Update baseline metrics
- Review and optimize code

### Retraining Trigger
```bash
# When performance drops below threshold
if r2 < 0.6:
    # Retrain model
    make train
    
    # Validate new model
    # If better, deploy
    # Update registry
```

## 📊 Metrics Dashboard

### Key Metrics to Track
- **Model Performance**: R², MAE, RMSE, MSE
- **Prediction Volume**: Predictions per hour/day
- **Response Time**: API latency
- **Error Rate**: Failed predictions
- **Data Drift**: Feature distribution changes
- **Model Drift**: Performance degradation over time

### Alert Thresholds
- R² < 0.6 → Retrain immediately
- MAE increase > 20% → Investigate
- Drift score > 0.2 → Data quality check
- Error rate > 5% → System health check

## 🎯 Best Practices

### 1. Version Control
- ✅ Version all models
- ✅ Track experiments
- ✅ Tag releases

### 2. Reproducibility
- ✅ Fixed random seeds
- ✅ Document dependencies
- ✅ Use Docker for deployment

### 3. Monitoring
- ✅ Log all predictions
- ✅ Track performance metrics
- ✅ Set up alerts

### 4. Testing
- ✅ Write unit tests
- ✅ Test before deployment
- ✅ Automate testing in CI/CD

### 5. Documentation
- ✅ Document code
- ✅ Maintain README
- ✅ Keep changelog

## 🚨 Troubleshooting

### Common Issues

**Model Performance Drops**
1. Check for data drift
2. Validate input data quality
3. Retrain with recent data
4. Consider feature engineering

**API Slow Response**
1. Check server resources
2. Increase workers in production
3. Optimize model loading
4. Use caching

**High Error Rate**
1. Check input validation
2. Review error logs
3. Add try-catch blocks
4. Improve error messages

---

For more details, see [README.md](README.md) and [SETUP.md](SETUP.md)
