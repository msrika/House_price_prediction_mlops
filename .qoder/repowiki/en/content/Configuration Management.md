# Configuration Management

<cite>
**Referenced Files in This Document**
- [config.yaml](file://configs/config.yaml)
- [config.example.yaml](file://configs/config.example.yaml)
- [config.py](file://src/config.py)
- [data.py](file://src/data.py)
- [model.py](file://src/model.py)
- [monitoring.py](file://src/monitoring.py)
- [tracking.py](file://src/tracking.py)
- [validation.py](file://src/validation.py)
- [docker-compose.yml](file://docker-compose.yml)
- [app.py](file://app.py)
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
9. [Conclusion](#conclusion)
10. [Appendices](#appendices)

## Introduction
This document explains the YAML-based configuration system used across the MLOps pipeline for house price prediction. It covers the structure of config.yaml, the Python configuration loader, environment-specific overrides, defaults, validation, and error handling. It also documents how configuration drives data loading, model training, experiment tracking, monitoring, and logging, and provides best practices for managing configuration across environments.

## Project Structure
The configuration system centers around a single YAML file and a small Python loader that exposes configuration values to the rest of the application. Supporting modules consume configuration to drive data ingestion, training, evaluation, monitoring, and experiment tracking.

```mermaid
graph TB
cfg["configs/config.yaml"]
ex["configs/config.example.yaml"]
loader["src/config.py"]
data_mod["src/data.py"]
model_mod["src/model.py"]
monitor_mod["src/monitoring.py"]
track_mod["src/tracking.py"]
valid_mod["src/validation.py"]
app["app.py"]
cfg --> loader
ex --> cfg
loader --> data_mod
loader --> model_mod
loader --> monitor_mod
loader --> track_mod
loader --> valid_mod
loader --> app
```

**Diagram sources**
- [config.yaml](file://configs/config.yaml)
- [config.example.yaml](file://configs/config.example.yaml)
- [config.py](file://src/config.py)
- [data.py](file://src/data.py)
- [model.py](file://src/model.py)
- [monitoring.py](file://src/monitoring.py)
- [tracking.py](file://src/tracking.py)
- [validation.py](file://src/validation.py)
- [app.py](file://app.py)

**Section sources**
- [config.yaml](file://configs/config.yaml)
- [config.example.yaml](file://configs/config.example.yaml)
- [config.py](file://src/config.py)

## Core Components
- YAML configuration file defines project metadata, data paths, model settings, training parameters, experiment tracking, monitoring thresholds, API settings, and logging configuration.
- The Python configuration loader reads YAML, supports nested key retrieval via dot notation, and provides convenience getters for common sections.
- Environment variables override selected runtime settings (for example, API port), while YAML remains the primary source of truth.

Key configuration areas:
- Project: name, version, description
- Data: raw and processed paths, splits, seeds
- Model: type, name, save path, metrics
- Training: solver parameters and early stopping
- Experiment: tracking URI and experiment name
- Monitoring: drift and performance thresholds, check frequency, alert contact
- API: host, port, debug flag, worker count
- Logging: level, format, file path

Practical customization examples:
- Adjust data paths: update raw and processed locations under data.
- Change model hyperparameters: adjust training parameters or model type/metrics.
- Set monitoring thresholds: tune drift and performance thresholds.
- Configure logging: change level, format, and output file.

Best practices:
- Keep secrets out of YAML; use environment variables or external secret stores.
- Maintain separate environment-specific YAML files or overlays.
- Version configuration alongside code and document breaking changes.
- Validate configuration at startup and fail fast on critical misconfiguration.

**Section sources**
- [config.yaml](file://configs/config.yaml)
- [config.example.yaml](file://configs/config.example.yaml)
- [config.py](file://src/config.py)
- [docker-compose.yml](file://docker-compose.yml)

## Architecture Overview
Configuration flows from YAML to the loader and then to all system components. The loader centralizes access and provides defaults. Some runtime values are overridden by environment variables.

```mermaid
sequenceDiagram
participant Y as "YAML config"
participant L as "Config loader"
participant D as "Data module"
participant M as "Model module"
participant T as "Tracking module"
participant N as "Monitoring module"
participant V as "Validation module"
participant A as "App"
Y->>L : "Load YAML"
L-->>D : "data.*"
L-->>M : "model.*, training.*"
L-->>T : "experiment.*"
L-->>N : "monitoring.*"
L-->>V : "monitoring.*"
L-->>A : "API settings"
A->>A : "Override port from env"
```

**Diagram sources**
- [config.py](file://src/config.py)
- [data.py](file://src/data.py)
- [model.py](file://src/model.py)
- [tracking.py](file://src/tracking.py)
- [monitoring.py](file://src/monitoring.py)
- [validation.py](file://src/validation.py)
- [app.py](file://app.py)

## Detailed Component Analysis

### YAML Configuration Structure
The YAML file organizes settings into logical groups:
- project: project metadata
- data: data paths and splits
- model: model type, name, save path, metrics
- training: solver and early stopping parameters
- experiment: MLflow-style tracking settings
- monitoring: drift and performance thresholds, alerting
- api: host, port, debug, workers
- logging: level, format, file

Example reference paths:
- Project metadata: [config.yaml](file://configs/config.yaml)
- Data paths and splits: [config.yaml](file://configs/config.yaml)
- Model settings and metrics: [config.yaml](file://configs/config.yaml)
- Training parameters: [config.yaml](file://configs/config.yaml)
- Experiment tracking: [config.yaml](file://configs/config.yaml)
- Monitoring thresholds: [config.yaml](file://configs/config.yaml)
- API settings: [config.yaml](file://configs/config.yaml)
- Logging configuration: [config.yaml](file://configs/config.yaml)

**Section sources**
- [config.yaml](file://configs/config.yaml)

### Python Configuration Loader
The loader:
- Reads YAML safely and returns a dictionary
- Provides dot-notation access to nested keys
- Returns defaults when keys are missing
- Exposes convenience getters for common sections

Key behaviors:
- Loads from a configurable path
- Gracefully handles missing files by returning an empty dictionary
- Supports nested retrieval for deep keys
- Offers helpers for data paths, model save path, training params, and monitoring config

```mermaid
classDiagram
class Config {
+__init__(config_path)
+_load_config() Dict
+get(key, default) Any
+get_project_name() str
+get_model_path() str
+get_data_paths() Dict
+get_training_params() Dict
+get_monitoring_config() Dict
}
```

**Diagram sources**
- [config.py](file://src/config.py)

**Section sources**
- [config.py](file://src/config.py)

### Data Loading and Preprocessing
Data components read configuration to locate datasets and control splits:
- DataLoader uses the configured raw path
- DataPreprocessor reads test size and random state from configuration
- Saves processed datasets to the configured processed directory

```mermaid
sequenceDiagram
participant C as "Config"
participant DL as "DataLoader"
participant DP as "DataPreprocessor"
C-->>DL : "data.raw_path"
DL->>DL : "load_data()"
C-->>DP : "data.test_size, data.random_state"
DP->>DP : "split_data()"
DP->>DP : "save_processed_data()"
```

**Diagram sources**
- [config.py](file://src/config.py)
- [data.py](file://src/data.py)

**Section sources**
- [data.py](file://src/data.py)
- [config.py](file://src/config.py)

### Model Training and Evaluation
Model components use configuration to select model type and training parameters:
- ModelTrainer creates and trains a model based on configuration
- Training parameters are read from configuration
- Model save path and name come from configuration

```mermaid
sequenceDiagram
participant C as "Config"
participant MT as "ModelTrainer"
participant ME as "ModelEvaluator"
C-->>MT : "model.type, training.*"
MT->>MT : "create_model()"
MT->>MT : "train()"
MT->>MT : "save_model()"
C-->>ME : "model.name"
ME->>ME : "evaluate()"
```

**Diagram sources**
- [config.py](file://src/config.py)
- [model.py](file://src/model.py)

**Section sources**
- [model.py](file://src/model.py)
- [config.py](file://src/config.py)

### Experiment Tracking
Experiment tracking reads configuration for experiment naming and persistence:
- Uses configured experiment name and tracking directory
- Logs runs, parameters, metrics, and artifacts
- Persists runs to JSON files for later inspection

```mermaid
sequenceDiagram
participant C as "Config"
participant ET as "ExperimentTracker"
C-->>ET : "experiment.experiment_name"
ET->>ET : "start_run()"
ET->>ET : "log_parameters(), log_metrics(), log_artifact()"
ET->>ET : "end_run()"
```

**Diagram sources**
- [config.py](file://src/config.py)
- [tracking.py](file://src/tracking.py)

**Section sources**
- [tracking.py](file://src/tracking.py)
- [config.py](file://src/config.py)

### Monitoring and Logging
Monitoring and logging components use configuration for thresholds and logging setup:
- MonitoringLogger initializes logging with configured level and format
- PerformanceMonitor applies configured thresholds for performance checks
- DriftDetector uses configured thresholds for drift detection

```mermaid
sequenceDiagram
participant C as "Config"
participant ML as "MonitoringLogger"
participant PM as "PerformanceMonitor"
participant DD as "DriftDetector"
C-->>ML : "logging.level, logging.format, logging.file"
ML->>ML : "setup logger"
C-->>PM : "monitoring.performance_threshold"
C-->>DD : "monitoring.drift_threshold"
PM->>PM : "check_performance()"
DD->>DD : "detect_drift()"
```

**Diagram sources**
- [config.py](file://src/config.py)
- [monitoring.py](file://src/monitoring.py)
- [validation.py](file://src/validation.py)

**Section sources**
- [monitoring.py](file://src/monitoring.py)
- [validation.py](file://src/validation.py)
- [config.py](file://src/config.py)

### API and Environment Overrides
The API server reads the port from an environment variable, allowing deployment platforms to override the default port without changing YAML:
- Port override: [app.py](file://app.py)
- Container environment variables: [docker-compose.yml](file://docker-compose.yml)

```mermaid
flowchart TD
Start(["Startup"]) --> ReadCfg["Read config.yaml"]
ReadCfg --> LoadEnv["Load environment variables"]
LoadEnv --> OverridePort{"PORT set?"}
OverridePort --> |Yes| UseEnvPort["Use PORT"]
OverridePort --> |No| UseCfgPort["Use config.api.port"]
UseEnvPort --> RunServer["Run server"]
UseCfgPort --> RunServer
RunServer --> End(["Ready"])
```

**Diagram sources**
- [app.py](file://app.py)
- [docker-compose.yml](file://docker-compose.yml)

**Section sources**
- [app.py](file://app.py)
- [docker-compose.yml](file://docker-compose.yml)

## Dependency Analysis
Configuration is consumed by multiple modules. The loader acts as a central dependency, while some modules depend on others indirectly (for example, monitoring depends on validation’s drift detector).

```mermaid
graph TB
cfg["configs/config.yaml"]
loader["src/config.py"]
data_mod["src/data.py"]
model_mod["src/model.py"]
monitor_mod["src/monitoring.py"]
track_mod["src/tracking.py"]
valid_mod["src/validation.py"]
app["app.py"]
cfg --> loader
loader --> data_mod
loader --> model_mod
loader --> monitor_mod
loader --> track_mod
loader --> valid_mod
loader --> app
monitor_mod --> valid_mod
```

**Diagram sources**
- [config.yaml](file://configs/config.yaml)
- [config.py](file://src/config.py)
- [data.py](file://src/data.py)
- [model.py](file://src/model.py)
- [monitoring.py](file://src/monitoring.py)
- [tracking.py](file://src/tracking.py)
- [validation.py](file://src/validation.py)
- [app.py](file://app.py)

**Section sources**
- [config.py](file://src/config.py)
- [data.py](file://src/data.py)
- [model.py](file://src/model.py)
- [monitoring.py](file://src/monitoring.py)
- [tracking.py](file://src/tracking.py)
- [validation.py](file://src/validation.py)
- [app.py](file://app.py)

## Performance Considerations
- Centralized configuration reduces repeated IO and parsing overhead.
- Using dot-notation access avoids deep nested lookups in hot paths.
- Prefer environment overrides for deployment-specific values (like port) to avoid re-parsing YAML during runtime.

## Troubleshooting Guide
Common issues and resolutions:
- Missing configuration file: The loader prints a message and returns an empty dictionary. Ensure the config path exists or set an environment override.
- Missing keys: The loader returns defaults; verify YAML structure and key names.
- Data path errors: Ensure raw and processed paths exist and are readable/writable.
- Model save/load failures: Confirm model save path permissions and that a model was trained.
- Monitoring thresholds: Tune drift and performance thresholds based on observed baselines.
- Logging misconfiguration: Verify logging level and file path; ensure the directory exists.

**Section sources**
- [config.py](file://src/config.py)
- [data.py](file://src/data.py)
- [model.py](file://src/model.py)
- [monitoring.py](file://src/monitoring.py)
- [validation.py](file://src/validation.py)

## Conclusion
The configuration system provides a clean separation between settings and logic. YAML defines behavior, the loader supplies defaults and accessors, and environment variables handle deployment-specific overrides. By following best practices—keeping secrets out of YAML, maintaining environment-specific files, and validating configuration at startup—you can achieve reliable, maintainable, and secure deployments.

## Appendices

### Practical Customization Examples
- Customize data paths:
  - Update raw and processed paths under data.
  - Reference: [config.yaml](file://configs/config.yaml)
- Adjust model hyperparameters:
  - Modify training parameters or model type/metrics.
  - Reference: [config.yaml](file://configs/config.yaml)
- Set monitoring thresholds:
  - Tune drift and performance thresholds.
  - Reference: [config.yaml](file://configs/config.yaml)
- Configure logging:
  - Change level, format, and output file.
  - Reference: [config.yaml](file://configs/config.yaml)

### Best Practices
- Secrets handling:
  - Store sensitive values in environment variables or secret managers; do not commit secrets to YAML.
- Environment-specific settings:
  - Maintain separate YAML files per environment (for example, dev, staging, prod) or use overlays.
- Configuration versioning:
  - Track changes to config.yaml alongside code; document breaking changes.
- Validation and defaults:
  - Validate configuration at startup and fail fast on critical misconfiguration.