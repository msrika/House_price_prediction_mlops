# Development Guidelines

<cite>
**Referenced Files in This Document**
- [README.md](file://README.md)
- [SETUP.md](file://SETUP.md)
- [QUICKSTART.md](file://QUICKSTART.md)
- [ARCHITECTURE.md](file://ARCHITECTURE.md)
- [MLOPS_WORKFLOW.md](file://MLOPS_WORKFLOW.md)
- [.pre-commit-config.yaml](file://.pre-commit-config.yaml)
- [pyproject.toml](file://pyproject.toml)
- [requirements-dev.txt](file://requirements-dev.txt)
- [Makefile](file://Makefile)
- [src/config.py](file://src/config.py)
- [src/data.py](file://src/data.py)
- [src/model.py](file://src/model.py)
- [src/validation.py](file://src/validation.py)
- [src/tracking.py](file://src/tracking.py)
- [src/monitoring.py](file://src/monitoring.py)
- [tests/test_components.py](file://tests/test_components.py)
</cite>

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
4. [Architecture Overview](#architecture-overview)
5. [Detailed Component Analysis](#detailed-component-analysis)
6. [Dependency Analysis](#dependency-analysis)
7. [Performance Considerations](#performance-considerations)
8. [Troubleshooting Guide](#troubleshooting-guide)
9. [Contribution Workflow](#contribution-workflow)
10. [Code Quality and Standards](#code-quality-and-standards)
11. [Development Environment Setup](#development-environment-setup)
12. [Debugging and Profiling](#debugging-and-profiling)
13. [Conclusion](#conclusion)

## Introduction
This document provides comprehensive development guidelines for the MLOps House Price Prediction project. It covers code standards, contribution workflows, best practices, development environment setup, quality checks, and operational guidance. The project follows modern MLOps practices with modular architecture, automated testing, experiment tracking, model registry, monitoring, and CI/CD readiness.

## Project Structure
The project is organized into clear functional areas:
- Source code: src/ with modules for configuration, data, model, validation, tracking, and monitoring
- Pipelines: pipelines/ containing training pipeline scripts
- Data: data/raw and data/processed for datasets
- Models: models/ and models/registry for persisted artifacts
- Tests: tests/ with unit tests
- Configuration: configs/config.yaml
- Dev tooling: Makefile, pyproject.toml, .pre-commit-config.yaml, requirements-dev.txt
- Documentation: README.md, SETUP.md, QUICKSTART.md, ARCHITECTURE.md, MLOPS_WORKFLOW.md

```mermaid
graph TB
A["Root"] --> B["src/"]
A --> C["pipelines/"]
A --> D["data/"]
A --> E["models/"]
A --> F["tests/"]
A --> G["configs/"]
A --> H["Makefile"]
A --> I[".pre-commit-config.yaml"]
A --> J["pyproject.toml"]
A --> K["requirements-dev.txt"]
B --> B1["config.py"]
B --> B2["data.py"]
B --> B3["model.py"]
B --> B4["validation.py"]
B --> B5["tracking.py"]
B --> B6["monitoring.py"]
```

**Diagram sources**
- [ARCHITECTURE.md](file://ARCHITECTURE.md)
- [src/config.py](file://src/config.py)
- [src/data.py](file://src/data.py)
- [src/model.py](file://src/model.py)
- [src/validation.py](file://src/validation.py)
- [src/tracking.py](file://src/tracking.py)
- [src/monitoring.py](file://src/monitoring.py)

**Section sources**
- [ARCHITECTURE.md](file://ARCHITECTURE.md)
- [README.md](file://README.md)

## Core Components
Key modules and their responsibilities:
- Configuration: centralized YAML-based configuration management
- Data: data loading, preprocessing, and saving processed datasets
- Model: training, evaluation, persistence, and loading of ML models
- Validation: data quality checks and drift detection
- Tracking: experiment runs and model registry
- Monitoring: structured logging, performance metrics, and alerts

Implementation highlights:
- Strong typing with type hints across modules
- Centralized configuration via a Config class
- Modular APIs for training, evaluation, validation, and monitoring
- JSON-based experiment tracking and model registry

**Section sources**
- [src/config.py](file://src/config.py)
- [src/data.py](file://src/data.py)
- [src/model.py](file://src/model.py)
- [src/validation.py](file://src/validation.py)
- [src/tracking.py](file://src/tracking.py)
- [src/monitoring.py](file://src/monitoring.py)

## Architecture Overview
The system follows a layered architecture:
- Presentation: Flask API serving predictions and dashboards
- Application: Python modules implementing ML workflows
- Data: CSV files and processed datasets
- Models: persisted artifacts with registry
- Observability: structured logs and metrics

```mermaid
graph TB
subgraph "Presentation Layer"
UI["Flask API<br/>Endpoints: /, /predict, /api/v1/predict, /health, /metrics"]
end
subgraph "Application Layer"
CFG["Config"]
DATA["Data Pipeline"]
MODEL["Model Pipeline"]
VALID["Validation"]
TRACK["Tracking"]
MON["Monitoring"]
end
subgraph "Data Layer"
RAW["Raw CSV"]
PROC["Processed CSV"]
MODELS["Models Registry"]
end
UI --> DATA
UI --> MODEL
UI --> VALID
UI --> TRACK
UI --> MON
DATA --> RAW
DATA --> PROC
MODEL --> MODELS
TRACK --> MODELS
MON --> MODELS
```

**Diagram sources**
- [ARCHITECTURE.md](file://ARCHITECTURE.md)
- [src/config.py](file://src/config.py)
- [src/data.py](file://src/data.py)
- [src/model.py](file://src/model.py)
- [src/validation.py](file://src/validation.py)
- [src/tracking.py](file://src/tracking.py)
- [src/monitoring.py](file://src/monitoring.py)

## Detailed Component Analysis

### Configuration Management
The Config class centralizes configuration loading and retrieval with dot-notation access for nested keys. It provides typed getters for project name, model paths, data paths, training parameters, and monitoring configuration.

```mermaid
classDiagram
class Config {
-str config_path
-dict config
+__init__(config_path="configs/config.yaml")
-_load_config() dict
+get(key, default=None) Any
+get_project_name() str
+get_model_path() str
+get_data_paths() dict
+get_training_params() dict
+get_monitoring_config() dict
}
```

**Diagram sources**
- [src/config.py](file://src/config.py)

**Section sources**
- [src/config.py](file://src/config.py)

### Data Pipeline
The data pipeline handles loading, validation, preprocessing, and saving processed datasets. It separates features and targets, splits into train/test sets, and persists processed data for reproducibility.

```mermaid
classDiagram
class DataLoader {
-str file_path
-DataFrame data
+__init__(file_path=None)
+load_data() DataFrame
+get_data_summary() dict
}
class DataPreprocessor {
-dict data_config
-DataFrame X_train
-DataFrame X_test
-Series y_train
-Series y_test
+__init__()
+prepare_features(df, target_column) tuple
+split_data(X, y, test_size=None, random_state=None) tuple
+save_processed_data(X_train, X_test, y_train, y_test) void
}
DataLoader --> DataPreprocessor : "feeds features/targets"
```

**Diagram sources**
- [src/data.py](file://src/data.py)

**Section sources**
- [src/data.py](file://src/data.py)

### Model Training and Evaluation
The model module creates, trains, evaluates, saves, and loads models. It supports multiple algorithms and computes standard regression metrics.

```mermaid
classDiagram
class ModelTrainer {
-str model_type
-BaseEstimator model
-dict training_params
+__init__(model_type="linear_regression")
+create_model() BaseEstimator
+train(X_train, y_train) BaseEstimator
+save_model(model_path=None, model_name=None) Path
+load_model(model_path) BaseEstimator
}
class ModelEvaluator {
-dict metrics
+__init__()
+evaluate(model, X_test, y_test) dict
+get_predictions(model, X) ndarray
+compare_models(models, X_test, y_test) DataFrame
+save_metrics(metrics, output_path) void
}
ModelTrainer --> ModelEvaluator : "produces model for evaluation"
```

**Diagram sources**
- [src/model.py](file://src/model.py)

**Section sources**
- [src/model.py](file://src/model.py)

### Validation and Drift Detection
DataValidator performs schema and quality checks, while DriftDetector compares distributions using multiple methods to detect data drift.

```mermaid
classDiagram
class DataValidator {
-dict schema
-dict validation_results
+__init__()
+define_schema(expected_columns, expected_dtypes) void
+validate_schema(df) tuple
+validate_data_quality(df) dict
+print_validation_report() void
}
class DriftDetector {
-float threshold
-dict reference_stats
-dict drift_results
+__init__(threshold=0.1)
+fit(reference_data) void
+detect_drift(current_data, method="ks_test") dict
+print_drift_report() void
}
DataValidator --> DriftDetector : "complementary checks"
```

**Diagram sources**
- [src/validation.py](file://src/validation.py)

**Section sources**
- [src/validation.py](file://src/validation.py)

### Experiment Tracking and Model Registry
ExperimentTracker logs runs with parameters, metrics, and artifacts. ModelRegistry manages model versions and metadata.

```mermaid
classDiagram
class ExperimentTracker {
-str experiment_name
-Path tracking_dir
-dict current_run
-list runs
+__init__(experiment_name=None)
+start_run(run_name=None) str
+log_parameters(params) void
+log_metrics(metrics) void
+log_artifact(artifact_path) void
+end_run(status="completed") void
+get_all_runs() list
+get_best_run(metric="r2", higher_is_better=True) dict
+compare_runs(metric="r2") DataFrame
}
class ModelRegistry {
-Path registry_dir
-Path metadata_file
-dict models
+__init__()
-_load_metadata() dict
+register_model(model_path, version, metrics, description="") dict
-_save_metadata() void
+get_model_version(version) dict
+get_latest_model() dict
+list_models() DataFrame
}
ExperimentTracker --> ModelRegistry : "outputs artifacts"
```

**Diagram sources**
- [src/tracking.py](file://src/tracking.py)

**Section sources**
- [src/tracking.py](file://src/tracking.py)

### Monitoring and Performance Alerts
MonitoringLogger logs predictions and performance metrics, while PerformanceMonitor compares current metrics against baselines to detect degradation.

```mermaid
classDiagram
class MonitoringLogger {
-Path log_dir
-Logger logger
-list predictions_log
-list performance_log
+__init__(log_dir="logs")
+log_prediction(input_data, prediction, confidence=None) dict
+log_performance(metrics, batch_id=None) dict
+log_drift_alert(drift_score, features) dict
+log_model_degradation(current_metric, baseline_metric, metric_name) dict
+save_logs() void
+get_prediction_summary() DataFrame
}
class PerformanceMonitor {
-float threshold
-dict baseline_metrics
-list alerts
+__init__(threshold=0.8)
+set_baseline(metrics) void
+check_performance(current_metrics) dict
+add_alert(alert_type, message, severity="WARNING") dict
+get_alerts() list
}
MonitoringLogger --> PerformanceMonitor : "consumes metrics"
```

**Diagram sources**
- [src/monitoring.py](file://src/monitoring.py)

**Section sources**
- [src/monitoring.py](file://src/monitoring.py)

## Dependency Analysis
The project relies on a curated set of libraries and tools:
- Runtime: Flask, scikit-learn, pandas, numpy, scipy, joblib
- Development: pytest, pytest-cov, flake8, mypy, black, isort, pre-commit
- DevOps: Docker, GitHub Actions (CI/CD), Makefile tasks

```mermaid
graph TB
subgraph "Runtime Dependencies"
FLASK["Flask"]
SKLEARN["scikit-learn"]
PANDAS["pandas"]
NUMPY["numpy"]
SCIPY["scipy"]
JOBLIB["joblib"]
end
subgraph "Dev Dependencies"
PYTEST["pytest"]
COV["pytest-cov"]
F8["flake8"]
MYPY["mypy"]
BLACK["black"]
ISORT["isort"]
PRECOMMIT["pre-commit"]
end
APP["Application"] --> FLASK
APP --> SKLEARN
APP --> PANDAS
APP --> NUMPY
APP --> SCIPY
APP --> JOBLIB
DEV["Developer Tools"] --> PYTEST
DEV --> COV
DEV --> F8
DEV --> MYPY
DEV --> BLACK
DEV --> ISORT
DEV --> PRECOMMIT
```

**Diagram sources**
- [requirements-dev.txt](file://requirements-dev.txt)
- [ARCHITECTURE.md](file://ARCHITECTURE.md)

**Section sources**
- [requirements-dev.txt](file://requirements-dev.txt)
- [ARCHITECTURE.md](file://ARCHITECTURE.md)

## Performance Considerations
- Use joblib for efficient model serialization, especially for large numpy arrays
- Persist processed datasets to reduce repeated preprocessing overhead
- Monitor prediction volume and response times; consider horizontal scaling with multiple Gunicorn workers
- Set baseline metrics and alert thresholds to detect performance degradation early
- Optimize model loading and consider caching strategies for inference

[No sources needed since this section provides general guidance]

## Troubleshooting Guide
Common issues and resolutions:
- Import errors: ensure virtual environment is activated and reinstall dependencies
- Port conflicts: change port in configuration
- Model not found: train a model first
- Test failures: reinstall development dependencies
- Data drift: investigate schema mismatches and quality issues
- API slowness: increase workers, optimize model loading, add caching

**Section sources**
- [SETUP.md](file://SETUP.md)
- [QUICKSTART.md](file://QUICKSTART.md)
- [MLOPS_WORKFLOW.md](file://MLOPS_WORKFLOW.md)

## Contribution Workflow
Follow these steps to contribute:
1. Fork the repository
2. Create a feature branch (git checkout -b feature/amazing-feature)
3. Commit changes (git commit -m 'Add amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request

Development guidelines:
- Write tests for new features
- Follow PEP 8 style guidelines
- Add type hints to functions
- Update documentation as needed
- Use meaningful commit messages

**Section sources**
- [README.md](file://README.md)

## Code Quality and Standards

### Coding Conventions
- PEP 8 compliance enforced via flake8 and black
- Type hints required for functions and classes
- Line length limit: 120 characters
- Black formatting profile aligned with isort

### Documentation Standards
- Docstrings for modules and classes
- Inline comments for complex logic
- README updates for new features
- Architecture and workflow documentation maintained

### Pre-commit Hooks and Linting
Configure pre-commit hooks to automate quality checks:
- trailing-whitespace, end-of-file-fixer
- YAML/JSON validation
- Large file detection
- Black formatting
- isort import sorting
- flake8 linting
- mypy type checking

Quality commands:
- make lint: run flake8
- make type-check: run mypy
- make format: run black and isort
- make test: run pytest with coverage

**Section sources**
- [.pre-commit-config.yaml](file://.pre-commit-config.yaml)
- [pyproject.toml](file://pyproject.toml)
- [Makefile](file://Makefile)

## Development Environment Setup
Recommended setup process:
1. Clone repository
2. Create virtual environment
3. Install dependencies (make install)
4. Setup project structure (make setup)
5. Verify installation (make test)

Quick start commands:
- make install: install production and development dependencies
- make setup: create required directories
- make train: run training pipeline
- make api: start development API server
- make test: run tests with coverage

**Section sources**
- [SETUP.md](file://SETUP.md)
- [QUICKSTART.md](file://QUICKSTART.md)
- [Makefile](file://Makefile)

## Debugging and Profiling
Debugging techniques:
- Use structured logging in MonitoringLogger
- Enable verbose test output (pytest -v)
- Print intermediate results during training
- Validate data quality before training

Profiling guidance:
- Monitor response times and error rates
- Track prediction volume trends
- Compare model performance metrics over time
- Use PerformanceMonitor to detect degradation

**Section sources**
- [src/monitoring.py](file://src/monitoring.py)
- [src/model.py](file://src/model.py)
- [tests/test_components.py](file://tests/test_components.py)

## Conclusion
This project establishes a robust foundation for MLOps development with clear architecture, comprehensive testing, experiment tracking, model registry, and monitoring. By following the development guidelines, contribution workflow, and quality standards outlined above, contributors can maintain code quality, ensure reproducibility, and support continuous delivery and monitoring in production.