# System Architecture and Design

<cite>
**Referenced Files in This Document**
- [app.py](file://House_Price_Prediction-main/housing1/app.py)
- [run_app.py](file://House_Price_Prediction-main/housing1/run_app.py)
- [src/__init__.py](file://House_Price_Prediction-main/housing1/src/__init__.py)
- [src/config.py](file://House_Price_Prediction-main/housing1/src/config.py)
- [src/data.py](file://House_Price_Prediction-main/housing1/src/data.py)
- [src/model.py](file://House_Price_Prediction-main/housing1/src/model.py)
- [src/validation.py](file://House_Price_Prediction-main/housing1/src/validation.py)
- [src/monitoring.py](file://House_Price_Prediction-main/housing1/src/monitoring.py)
- [src/tracking.py](file://House_Price_Prediction-main/housing1/src/tracking.py)
- [visualization.py](file://House_Price_Prediction-main/housing1/visualization.py)
- [configs/config.yaml](file://House_Price_Prediction-main/housing1/configs/config.yaml)
- [Dockerfile](file://House_Price_Prediction-main/housing1/Dockerfile)
- [docker-compose.yml](file://House_Price_Prediction-main/housing1/docker-compose.yml)
- [.github/workflows/mlops_pipeline.yml](file://House_Price_Prediction-main/housing1/.github/workflows/mlops_pipeline.yml)
- [requirements.txt](file://House_Price_Prediction-main/housing1/requirements.txt)
- [templates/index.html](file://House_Price_Prediction-main/housing1/templates/index.html)
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
This document describes the system architecture and design of the House Price Prediction system. It explains the high-level design patterns (modular architecture, MVC-like separation, factory pattern for model creation, strategy pattern for interchangeable model implementations, and configuration pattern for centralized settings), component interactions among the Flask application, data processing modules, machine learning components, and monitoring systems, and the end-to-end data flow from CSV loading through model inference to web interface rendering. It also covers system boundaries, integration patterns, technical decisions, infrastructure requirements, scalability considerations, deployment topology, and MLOps principles embedded in the design.

## Project Structure
The project follows a modular layout with clear separation of concerns:
- Web application entrypoint and routes
- Source modules for configuration, data, modeling, validation, monitoring, and experiment tracking
- Visualization utilities
- Configuration files and templates
- Containerization and orchestration assets
- GitHub Actions CI/CD pipeline

```mermaid
graph TB
subgraph "Web Layer"
A["Flask App<br/>app.py"]
T["Templates<br/>templates/index.html"]
end
subgraph "Source Modules"
C["Config<br/>src/config.py"]
D["Data<br/>src/data.py"]
M["Model<br/>src/model.py"]
V["Validation<br/>src/validation.py"]
MON["Monitoring<br/>src/monitoring.py"]
TR["Tracking<br/>src/tracking.py"]
VZ["Visualization<br/>visualization.py"]
end
subgraph "Artifacts"
CFG["Config YAML<br/>configs/config.yaml"]
DATA["CSV Data<br/>Data/house_price.csv"]
MODELS["Models<br/>models/*.pkl"]
LOGS["Logs<br/>logs/*.log"]
EXP["Experiments<br/>experiments/*.json"]
end
subgraph "Runtime"
Gunicorn["WSGI Server<br/>Gunicorn"]
Docker["Container Runtime<br/>Docker"]
Compose["Compose Orchestration<br/>docker-compose.yml"]
end
A --> T
A --> C
A --> D
A --> M
A --> VZ
D --> C
M --> C
V --> C
MON --> C
TR --> C
A --> DATA
M --> MODELS
MON --> LOGS
TR --> EXP
Gunicorn --> A
Docker --> Gunicorn
Compose --> Docker
```

**Diagram sources**
- [app.py:1-113](file://House_Price_Prediction-main/housing1/app.py#L1-L113)
- [templates/index.html:1-145](file://House_Price_Prediction-main/housing1/templates/index.html#L1-L145)
- [src/config.py:1-63](file://House_Price_Prediction-main/housing1/src/config.py#L1-L63)
- [src/data.py:1-109](file://House_Price_Prediction-main/housing1/src/data.py#L1-L109)
- [src/model.py:1-155](file://House_Price_Prediction-main/housing1/src/model.py#L1-L155)
- [src/validation.py:1-243](file://House_Price_Prediction-main/housing1/src/validation.py#L1-L243)
- [src/monitoring.py:1-218](file://House_Price_Prediction-main/housing1/src/monitoring.py#L1-L218)
- [src/tracking.py:1-218](file://House_Price_Prediction-main/housing1/src/tracking.py#L1-L218)
- [visualization.py:1-348](file://House_Price_Prediction-main/housing1/visualization.py#L1-L348)
- [configs/config.yaml:1-60](file://House_Price_Prediction-main/housing1/configs/config.yaml#L1-L60)
- [Dockerfile:1-39](file://House_Price_Prediction-main/housing1/Dockerfile#L1-L39)
- [docker-compose.yml:1-52](file://House_Price_Prediction-main/housing1/docker-compose.yml#L1-L52)

**Section sources**
- [app.py:1-113](file://House_Price_Prediction-main/housing1/app.py#L1-L113)
- [templates/index.html:1-145](file://House_Price_Prediction-main/housing1/templates/index.html#L1-L145)
- [configs/config.yaml:1-60](file://House_Price_Prediction-main/housing1/configs/config.yaml#L1-L60)
- [Dockerfile:1-39](file://House_Price_Prediction-main/housing1/Dockerfile#L1-L39)
- [docker-compose.yml:1-52](file://House_Price_Prediction-main/housing1/docker-compose.yml#L1-L52)

## Core Components
- Flask application: Provides routes for prediction, visualization, and dashboard rendering, integrates with visualization utilities, and loads a pre-trained model for inference.
- Data layer: Loads CSV data, validates schema and quality, prepares features, splits datasets, and persists processed artifacts.
- Model layer: Factory-style model creation supporting multiple regressors, training, evaluation, persistence, and loading.
- Validation and drift detection: Validates data schema and quality, detects feature drift using configurable methods.
- Monitoring and logging: Logs predictions and performance, tracks drift alerts, and maintains structured logs.
- Experiment tracking and registry: Tracks experiment runs, logs parameters and metrics, and registers model versions.
- Visualization: Generates static charts and interactive dashboards for insights and performance analysis.
- Configuration: Centralized YAML-based configuration for project, data, model, training, monitoring, API, and logging settings.
- Packaging and runtime: Docker containerization with Gunicorn, orchestrated via docker-compose.

**Section sources**
- [app.py:1-113](file://House_Price_Prediction-main/housing1/app.py#L1-L113)
- [src/data.py:1-109](file://House_Price_Prediction-main/housing1/src/data.py#L1-L109)
- [src/model.py:1-155](file://House_Price_Prediction-main/housing1/src/model.py#L1-L155)
- [src/validation.py:1-243](file://House_Price_Prediction-main/housing1/src/validation.py#L1-L243)
- [src/monitoring.py:1-218](file://House_Price_Prediction-main/housing1/src/monitoring.py#L1-L218)
- [src/tracking.py:1-218](file://House_Price_Prediction-main/housing1/src/tracking.py#L1-L218)
- [visualization.py:1-348](file://House_Price_Prediction-main/housing1/visualization.py#L1-L348)
- [src/config.py:1-63](file://House_Price_Prediction-main/housing1/src/config.py#L1-L63)

## Architecture Overview
The system employs a layered, modular architecture with clear separation between presentation, business logic, data, and model components. It follows an MVC-like pattern at the web layer (routes and templates), while the backend encapsulates data processing, model management, validation, monitoring, and experiment tracking as cohesive modules. A configuration-driven approach centralizes settings, enabling easy adaptation across environments.

```mermaid
graph TB
Client["Browser"]
Routes["Flask Routes<br/>app.py"]
Controller["Controller Logic<br/>app.py"]
View["Template Rendering<br/>templates/index.html"]
Viz["DataVisualizer<br/>visualization.py"]
DL["DataLoader<br/>src/data.py"]
DP["DataPreprocessor<br/>src/data.py"]
MT["ModelTrainer<br/>src/model.py"]
ME["ModelEvaluator<br/>src/model.py"]
VAL["DataValidator/DriftDetector<br/>src/validation.py"]
MON["MonitoringLogger/PerformanceMonitor<br/>src/monitoring.py"]
TRK["ExperimentTracker/ModelRegistry<br/>src/tracking.py"]
CFG["Config Manager<br/>src/config.py"]
YAML["Config YAML<br/>configs/config.yaml"]
Client --> Routes
Routes --> Controller
Controller --> View
Controller --> Viz
Controller --> DL
Controller --> DP
Controller --> MT
Controller --> ME
Controller --> VAL
Controller --> MON
Controller --> TRK
CFG --> YAML
DL --> CFG
DP --> CFG
MT --> CFG
ME --> CFG
VAL --> CFG
MON --> CFG
TRK --> CFG
```

**Diagram sources**
- [app.py:1-113](file://House_Price_Prediction-main/housing1/app.py#L1-L113)
- [templates/index.html:1-145](file://House_Price_Prediction-main/housing1/templates/index.html#L1-L145)
- [visualization.py:1-348](file://House_Price_Prediction-main/housing1/visualization.py#L1-L348)
- [src/data.py:1-109](file://House_Price_Prediction-main/housing1/src/data.py#L1-L109)
- [src/model.py:1-155](file://House_Price_Prediction-main/housing1/src/model.py#L1-L155)
- [src/validation.py:1-243](file://House_Price_Prediction-main/housing1/src/validation.py#L1-L243)
- [src/monitoring.py:1-218](file://House_Price_Prediction-main/housing1/src/monitoring.py#L1-L218)
- [src/tracking.py:1-218](file://House_Price_Prediction-main/housing1/src/tracking.py#L1-L218)
- [src/config.py:1-63](file://House_Price_Prediction-main/housing1/src/config.py#L1-L63)
- [configs/config.yaml:1-60](file://House_Price_Prediction-main/housing1/configs/config.yaml#L1-L60)

## Detailed Component Analysis

### Flask Application (Presentation and Routing)
- Responsibilities: Serve HTML templates, accept form submissions, perform inference using a preloaded model, and render results or visualizations.
- Key flows:
  - GET "/" renders the prediction form.
  - POST "/predict" reads form inputs, constructs a feature vector, predicts price, and returns a rendered page with the result.
  - GET "/visualize" generates and displays static charts and metrics.
  - GET "/dashboard" creates an interactive Plotly dashboard.
- Production runtime: Uses Gunicorn via Docker and docker-compose.

```mermaid
sequenceDiagram
participant U as "User"
participant F as "Flask app.py"
participant V as "DataVisualizer"
participant M as "Pretrained Model"
U->>F : "GET /"
F-->>U : "Render index.html (Prediction Form)"
U->>F : "POST /predict with form data"
F->>F : "Parse inputs and construct array"
F->>M : "predict(array)"
M-->>F : "prediction"
F-->>U : "Render index.html with prediction result"
U->>F : "GET /visualize"
F->>V : "create_* charts and metrics"
V-->>F : "base64 images + metrics"
F-->>U : "Render index.html with visualizations"
U->>F : "GET /dashboard"
F->>V : "create_interactive_dashboard()"
V-->>F : "HTML iframe"
F-->>U : "Render index.html with dashboard"
```

**Diagram sources**
- [app.py:37-113](file://House_Price_Prediction-main/housing1/app.py#L37-L113)
- [visualization.py:23-317](file://House_Price_Prediction-main/housing1/visualization.py#L23-L317)

**Section sources**
- [app.py:1-113](file://House_Price_Prediction-main/housing1/app.py#L1-L113)
- [templates/index.html:1-145](file://House_Price_Prediction-main/housing1/templates/index.html#L1-L145)

### Data Processing Module (DataLoader, DataPreprocessor)
- DataLoader: Loads CSV data with robust error handling and prints summary statistics.
- DataPreprocessor: Separates features/target, splits into train/test sets using configuration-driven parameters, and saves processed datasets.

```mermaid
flowchart TD
Start(["Start Data Processing"]) --> Load["Load CSV via DataLoader"]
Load --> ValidateSchema["Validate Schema and Quality"]
ValidateSchema --> Prepare["Prepare Features and Target"]
Prepare --> Split["Split into Train/Test Sets"]
Split --> Save["Save Processed Data"]
Save --> End(["End"])
```

**Diagram sources**
- [src/data.py:13-109](file://House_Price_Prediction-main/housing1/src/data.py#L13-L109)

**Section sources**
- [src/data.py:1-109](file://House_Price_Prediction-main/housing1/src/data.py#L1-L109)
- [configs/config.yaml:9-16](file://House_Price_Prediction-main/housing1/configs/config.yaml#L9-L16)

### Model Management (ModelTrainer, ModelEvaluator)
- ModelTrainer: Factory-style creation of linear regression, random forest, or gradient boosting models based on configuration; supports training, saving, and loading.
- ModelEvaluator: Computes MAE, MSE, RMSE, R²; compares multiple models; persists metrics.

```mermaid
classDiagram
class ModelTrainer {
+string model_type
+create_model() Model
+train(X_train, y_train) Model
+save_model(model_path, model_name) Path
+load_model(model_path) Model
}
class ModelEvaluator {
+evaluate(model, X_test, y_test) Dict
+get_predictions(model, X) ndarray
+compare_models(models, X_test, y_test) DataFrame
+save_metrics(metrics, output_path) void
}
ModelTrainer --> ModelEvaluator : "evaluates trained models"
```

**Diagram sources**
- [src/model.py:17-155](file://House_Price_Prediction-main/housing1/src/model.py#L17-L155)

**Section sources**
- [src/model.py:1-155](file://House_Price_Prediction-main/housing1/src/model.py#L1-L155)
- [configs/config.yaml:17-27](file://House_Price_Prediction-main/housing1/configs/config.yaml#L17-L27)

### Validation and Drift Detection
- DataValidator: Enforces schema and reports quality metrics including missing values, duplicates, and outlier counts.
- DriftDetector: Computes drift using KS-test, PSI, or mean-shift thresholds against reference statistics.

```mermaid
flowchart TD
A["Reference Data"] --> Fit["Fit Reference Statistics"]
B["Current Data"] --> Detect["Detect Drift per Feature"]
Detect --> Report["Generate Drift Report"]
Report --> Alert{"Drift Detected?"}
Alert --> |Yes| LogAlert["Log Drift Alert"]
Alert --> |No| OK["No Action"]
```

**Diagram sources**
- [src/validation.py:124-243](file://House_Price_Prediction-main/housing1/src/validation.py#L124-L243)

**Section sources**
- [src/validation.py:1-243](file://House_Price_Prediction-main/housing1/src/validation.py#L1-L243)
- [configs/config.yaml:41-47](file://House_Price_Prediction-main/housing1/configs/config.yaml#L41-L47)

### Monitoring and Logging
- MonitoringLogger: Logs predictions, performance metrics, drift alerts, and degradations; persists logs to JSON files.
- PerformanceMonitor: Compares current metrics to baseline thresholds and raises alerts.

```mermaid
sequenceDiagram
participant F as "Flask app.py"
participant MON as "MonitoringLogger"
participant PM as "PerformanceMonitor"
F->>MON : "log_prediction(input, prediction)"
MON-->>F : "entry"
F->>PM : "check_performance(current_metrics)"
PM-->>F : "pass/fail + violations"
F->>MON : "log_performance(metrics)"
MON-->>F : "entry"
```

**Diagram sources**
- [src/monitoring.py:15-218](file://House_Price_Prediction-main/housing1/src/monitoring.py#L15-L218)
- [app.py:42-66](file://House_Price_Prediction-main/housing1/app.py#L42-L66)

**Section sources**
- [src/monitoring.py:1-218](file://House_Price_Prediction-main/housing1/src/monitoring.py#L1-L218)
- [configs/config.yaml:41-47](file://House_Price_Prediction-main/housing1/configs/config.yaml#L41-L47)

### Experiment Tracking and Registry
- ExperimentTracker: Starts runs, logs parameters and metrics, saves artifacts, and compiles run comparisons.
- ModelRegistry: Registers model versions with metadata, copies artifacts, and lists versions.

```mermaid
classDiagram
class ExperimentTracker {
+start_run(run_name) string
+log_parameters(params) void
+log_metrics(metrics) void
+log_artifact(artifact_path) void
+end_run(status) void
+get_all_runs() List
+get_best_run(metric, higher_is_better) Dict
+compare_runs(metric) DataFrame
}
class ModelRegistry {
+register_model(model_path, version, metrics, description) Dict
+get_model_version(version) Dict
+get_latest_model() Dict
+list_models() DataFrame
}
```

**Diagram sources**
- [src/tracking.py:14-218](file://House_Price_Prediction-main/housing1/src/tracking.py#L14-L218)

**Section sources**
- [src/tracking.py:1-218](file://House_Price_Prediction-main/housing1/src/tracking.py#L1-L218)
- [configs/config.yaml:35-40](file://House_Price_Prediction-main/housing1/configs/config.yaml#L35-L40)

### Visualization Utilities
- DataVisualizer: Loads data, computes correlations, distributions, scatter plots, performance charts, and interactive dashboards; returns base64-encoded images or Plotly HTML.

```mermaid
flowchart TD
VStart["Initialize DataVisualizer"] --> Load["Load CSV"]
Load --> Corr["Correlation Heatmap"]
Load --> Dist["Feature Distributions"]
Load --> Scatter["Scatter vs Price"]
Load --> Perf["Model Performance Charts"]
Load --> Dash["Interactive Dashboard"]
Corr --> VEnd["Return Base64 Images"]
Dist --> VEnd
Scatter --> VEnd
Perf --> VEnd
Dash --> VEnd
```

**Diagram sources**
- [visualization.py:23-317](file://House_Price_Prediction-main/housing1/visualization.py#L23-L317)

**Section sources**
- [visualization.py:1-348](file://House_Price_Prediction-main/housing1/visualization.py#L1-L348)

### Configuration Pattern
- Centralized YAML configuration drives project metadata, data paths, model settings, training parameters, monitoring thresholds, API settings, and logging format.
- Config class provides safe access with nested key resolution and defaults.

```mermaid
flowchart TD
Yaml["configs/config.yaml"] --> Loader["Config YAML Loader"]
Loader --> Access["Config.get(key)"]
Access --> Data["Data Paths"]
Access --> Model["Model Paths"]
Access --> Train["Training Params"]
Access --> Mon["Monitoring Config"]
Access --> API["API Config"]
Access --> Log["Logging Config"]
```

**Diagram sources**
- [configs/config.yaml:1-60](file://House_Price_Prediction-main/housing1/configs/config.yaml#L1-L60)
- [src/config.py:10-63](file://House_Price_Prediction-main/housing1/src/config.py#L10-L63)

**Section sources**
- [src/config.py:1-63](file://House_Price_Prediction-main/housing1/src/config.py#L1-L63)
- [configs/config.yaml:1-60](file://House_Price_Prediction-main/housing1/configs/config.yaml#L1-L60)

## Dependency Analysis
The system exhibits low coupling and high cohesion across modules, with explicit dependencies flowing from the Flask app to data, model, validation, monitoring, and tracking modules. Configuration is injected centrally to avoid hardcoding.

```mermaid
graph LR
APP["app.py"] --> CFG["src/config.py"]
APP --> DATA["src/data.py"]
APP --> MODEL["src/model.py"]
APP --> VIZ["visualization.py"]
DATA --> CFG
MODEL --> CFG
VAL["src/validation.py"] --> CFG
MON["src/monitoring.py"] --> CFG
TRK["src/tracking.py"] --> CFG
```

**Diagram sources**
- [app.py:1-113](file://House_Price_Prediction-main/housing1/app.py#L1-L113)
- [src/config.py:1-63](file://House_Price_Prediction-main/housing1/src/config.py#L1-L63)
- [src/data.py:1-109](file://House_Price_Prediction-main/housing1/src/data.py#L1-L109)
- [src/model.py:1-155](file://House_Price_Prediction-main/housing1/src/model.py#L1-L155)
- [src/validation.py:1-243](file://House_Price_Prediction-main/housing1/src/validation.py#L1-L243)
- [src/monitoring.py:1-218](file://House_Price_Prediction-main/housing1/src/monitoring.py#L1-L218)
- [src/tracking.py:1-218](file://House_Price_Prediction-main/housing1/src/tracking.py#L1-L218)
- [visualization.py:1-348](file://House_Price_Prediction-main/housing1/visualization.py#L1-L348)

**Section sources**
- [requirements.txt:1-24](file://House_Price_Prediction-main/housing1/requirements.txt#L1-L24)

## Performance Considerations
- Model persistence: Uses joblib for efficient serialization of scikit-learn estimators.
- Visualization: Non-interactive Matplotlib backend ensures headless operation; images are base64-encoded for inline rendering.
- Data processing: Efficient pandas operations and train/test split with configurable parameters.
- Scalability: Containerized deployment with Gunicorn allows horizontal scaling via multiple workers; docker-compose exposes health checks for readiness.

[No sources needed since this section provides general guidance]

## Troubleshooting Guide
- Data loading errors: DataLoader raises explicit exceptions if the CSV is missing or unreadable.
- Schema and quality issues: DataValidator reports missing columns, dtype mismatches, duplicates, and outlier counts.
- Drift detection: DriftDetector requires reference statistics; ensure fit() is called before detect_drift().
- Monitoring: MonitoringLogger writes structured logs; verify log directory permissions and timestamps.
- Experiment tracking: ExperimentTracker saves runs as JSON; confirm experiment directories exist.
- Model registry: ModelRegistry copies artifacts; ensure destination paths are writable.
- Flask routes: POST /predict expects numeric form fields; invalid inputs trigger error handling and render an error message.

**Section sources**
- [src/data.py:20-31](file://House_Price_Prediction-main/housing1/src/data.py#L20-L31)
- [src/validation.py:28-50](file://House_Price_Prediction-main/housing1/src/validation.py#L28-L50)
- [src/validation.py:132-151](file://House_Price_Prediction-main/housing1/src/validation.py#L132-L151)
- [src/monitoring.py:122-139](file://House_Price_Prediction-main/housing1/src/monitoring.py#L122-L139)
- [src/tracking.py:75-83](file://House_Price_Prediction-main/housing1/src/tracking.py#L75-L83)
- [app.py:42-66](file://House_Price_Prediction-main/housing1/app.py#L42-L66)

## Conclusion
The House Price Prediction system demonstrates a clean, modular architecture that separates concerns across data, model, validation, monitoring, and experiment tracking modules. It leverages configuration-driven settings, a factory-style model creation pattern, and a strategy-like selection of model implementations. The Flask application provides a straightforward MVC-like interface, while Docker and docker-compose enable containerized, scalable deployments. The MLOps pipeline integrates testing, validation, and deployment automation, ensuring reliability and reproducibility.

[No sources needed since this section summarizes without analyzing specific files]

## Appendices

### System Context Diagram
```mermaid
graph TB
subgraph "External"
Users["Users/Browser"]
CI["GitHub Actions"]
end
subgraph "Application"
Web["Flask App"]
Gunicorn["Gunicorn"]
Docker["Docker Runtime"]
Compose["docker-compose"]
end
subgraph "Data and Artifacts"
CSV["CSV Data"]
Models["Trained Models"]
Logs["Logs"]
Experiments["Experiment Runs"]
end
subgraph "Modules"
Config["Config"]
Data["Data Processing"]
Model["Model Management"]
Val["Validation"]
Mon["Monitoring"]
Track["Experiment Tracking"]
Viz["Visualization"]
end
Users --> Web
CI --> Docker
Docker --> Gunicorn
Gunicorn --> Web
Web --> Config
Web --> Data
Web --> Model
Web --> Val
Web --> Mon
Web --> Track
Web --> Viz
Data --> CSV
Model --> Models
Mon --> Logs
Track --> Experiments
Compose --> Docker
```

**Diagram sources**
- [app.py:1-113](file://House_Price_Prediction-main/housing1/app.py#L1-L113)
- [Dockerfile:1-39](file://House_Price_Prediction-main/housing1/Dockerfile#L1-L39)
- [docker-compose.yml:1-52](file://House_Price_Prediction-main/housing1/docker-compose.yml#L1-L52)
- [.github/workflows/mlops_pipeline.yml:1-180](file://House_Price_Prediction-main/housing1/.github/workflows/mlops_pipeline.yml#L1-L180)

### Data Flow from CSV to Web Rendering
```mermaid
flowchart TD
CSV["CSV File"] --> DL["DataLoader"]
DL --> DP["DataPreprocessor"]
DP --> MT["ModelTrainer"]
MT --> SAVE["Save Model"]
SAVE --> WEB["Flask App"]
WEB --> PRED["Inference"]
WEB --> VIZ["Visualization"]
WEB --> RENDER["Render Template"]
```

**Diagram sources**
- [src/data.py:20-109](file://House_Price_Prediction-main/housing1/src/data.py#L20-L109)
- [src/model.py:62-87](file://House_Price_Prediction-main/housing1/src/model.py#L62-L87)
- [app.py:42-113](file://House_Price_Prediction-main/housing1/app.py#L42-L113)
- [templates/index.html:1-145](file://House_Price_Prediction-main/housing1/templates/index.html#L1-L145)

### Technology Stack and Compatibility
- Core: Flask, NumPy, Pandas, scikit-learn, SciPy
- Visualization: Matplotlib, Seaborn, Plotly
- Monitoring: Prometheus client
- Production: Gunicorn
- Packaging: Docker
- CI/CD: GitHub Actions

**Section sources**
- [requirements.txt:1-24](file://House_Price_Prediction-main/housing1/requirements.txt#L1-L24)

### Deployment Topology and Infrastructure
- Single-service container exposing port 5000, with persistent volumes for data, models, logs, and experiments.
- Health checks configured for readiness.
- Environment variables support host binding and worker count.

**Section sources**
- [Dockerfile:1-39](file://House_Price_Prediction-main/housing1/Dockerfile#L1-L39)
- [docker-compose.yml:1-52](file://House_Price_Prediction-main/housing1/docker-compose.yml#L1-L52)

### MLOps Principles Integrated
- Centralized configuration for reproducibility.
- Experiment tracking with parameter and metric logging.
- Model registry for versioning and provenance.
- Automated CI/CD pipeline with linting, testing, type checking, model validation, and staged deployments.
- Monitoring and logging for observability.

**Section sources**
- [configs/config.yaml:1-60](file://House_Price_Prediction-main/housing1/configs/config.yaml#L1-L60)
- [src/tracking.py:14-218](file://House_Price_Prediction-main/housing1/src/tracking.py#L14-L218)
- [src/monitoring.py:15-218](file://House_Price_Prediction-main/housing1/src/monitoring.py#L15-L218)
- [.github/workflows/mlops_pipeline.yml:1-180](file://House_Price_Prediction-main/housing1/.github/workflows/mlops_pipeline.yml#L1-L180)