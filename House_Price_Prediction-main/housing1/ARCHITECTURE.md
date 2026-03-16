# 🏗️ MLOps Architecture

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                           │
│                    (Web Browser / API Client)                    │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP/REST API
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API Layer (Flask)                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  /predict    │  │   /health    │  │   /metrics   │          │
│  │  Endpoint    │  │   Endpoint   │  │  Endpoint    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Application Logic                            │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              src/ Modules                               │    │
│  │                                                         │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐             │    │
│  │  │ config   │  │  data    │  │  model   │             │    │
│  │  │ Manager  │  │ Pipeline │  │ Trainer  │             │    │
│  │  └──────────┘  └──────────┘  └──────────┘             │    │
│  │                                                         │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐             │    │
│  │  │tracking  │  │validation│  │monitoring│             │    │
│  │  │Registry  │  │ & Drift  │  │ Logger   │             │    │
│  │  └──────────┘  └──────────┘  └──────────┘             │    │
│  └────────────────────────────────────────────────────────┘    │
└────────────────────────┬────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│   Data      │ │   Models    │ │    Logs     │
│  Storage    │ │  Registry   │ │   Files     │
│             │ │             │ │             │
│ ┌─────────┐ │ │ ┌─────────┐ │ │ ┌─────────┐ │
│ │Raw CSV  │ │ │ │Model v1 │ │ │ │app.log  │ │
│ │Proc CSV │ │ │ │Model v2 │ │ │ │monitor  │ │
│ └─────────┘ │ │ └─────────┘ │ │ │pred.log │ │
└─────────────┘ └─────────────┘ └─────────────┘
```

## Data Flow Architecture

### Training Pipeline Flow

```
Data Source → Validation → Preprocessing → Training → Evaluation → Registry
     │            │              │              │           │          │
     │            │              │              │           │          │
     ▼            ▼              ▼              ▼           ▼          ▼
  Raw CSV    Quality       Features &     Model      Metrics    Versioned
            Check         Targets        Train      Report      Model
```

### Prediction Flow

```
API Request → Validation → Feature Prep → Model Load → Prediction → Response
     │            │             │             │            │           │
     │            │             │             │            │           │
     ▼            ▼             ▼             ▼            ▼           ▼
  JSON/Form   Schema       Transform     Latest       Price      JSON/HTML
             Check                      Version      Estimate
```

### Monitoring Flow

```
Prediction → Logging → Metrics Store → Analysis → Alerts
     │          │           │              │          │
     │          │           │              │          │
     ▼          ▼           ▼              ▼          ▼
  Input &    Track      Aggregate    Compare to   If threshold
 Output     Stats       Trends       Baseline     breached
```

## Component Interactions

### 1. Configuration Management

```
┌──────────────────┐
│  config.yaml     │◄─── Central configuration
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Config Class    │◄─── Used by all modules
└──────────────────┘
```

### 2. Data Pipeline

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│ DataLoader  │─────▶│Preprocessor │─────▶│  Validator  │
└─────────────┘      └─────────────┘      └─────────────┘
       │                    │                    │
       ▼                    ▼                    ▼
  Load CSV              Split              Quality
                        Train/Test         Check
```

### 3. Model Lifecycle

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Create   │───▶│  Train   │───▶│ Evaluate │───▶│  Save    │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                                           │
                                           ▼
                                    ┌──────────┐
                                    │ Register │
                                    └──────────┘
```

### 4. Experiment Tracking

```
┌─────────────┐
│ Start Run   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Log Params  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Log Metrics │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  End Run    │
└─────────────┘
```

## Deployment Architecture

### Development Environment

```
┌─────────────────────────────────────┐
│     Local Machine                   │
│                                     │
│  ┌───────────┐  ┌───────────────┐  │
│  │ Flask App │  │  Test Suite   │  │
│  │ :5000     │  │  pytest       │  │
│  └───────────┘  └───────────────┘  │
└─────────────────────────────────────┘
```

### Production Environment (Docker)

```
┌─────────────────────────────────────┐
│     Docker Container                │
│                                     │
│  ┌───────────┐  ┌───────────────┐  │
│  │ Gunicorn  │  │  Flask App    │  │
│  │ 4 Workers │  │  api.py       │  │
│  └───────────┘  └───────────────┘  │
│                                     │
│  ┌───────────┐  ┌───────────────┐  │
│  │  Models   │  │    Logs       │  │
│  └───────────┘  └───────────────┘  │
└─────────────────────────────────────┘
```

### CI/CD Pipeline Architecture

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│   Push   │────▶│  Test    │────▶│  Build   │
│  Code    │     │  Suite    │     │  Image   │
└──────────┘     └──────────┘     └──────────┘
                                          │
                                          ▼
                                   ┌──────────┐
                                   │ Deploy   │
                                   │ Staging  │
                                   └──────────┘
                                          │
                                          ▼
                                   ┌──────────┐
                                   │ Deploy   │
                                   │Production│
                                   └──────────┘
```

## Technology Stack

### Backend
- **Python 3.10+**: Core language
- **Flask**: Web framework
- **Gunicorn**: WSGI server
- **scikit-learn**: ML library

### Data & ML
- **pandas**: Data manipulation
- **numpy**: Numerical computing
- **scipy**: Scientific computing
- **joblib**: Model serialization

### DevOps
- **Docker**: Containerization
- **GitHub Actions**: CI/CD
- **pytest**: Testing
- **flake8/black**: Code quality

### Monitoring
- **Custom logging**: Application logs
- **JSON logs**: Structured logging
- **Metrics tracking**: Performance monitoring

## Security Considerations

```
┌─────────────────────────────────────┐
│         Security Layers             │
│                                     │
│  ┌─────────────────────────────┐   │
│  │  Input Validation           │   │
│  │  - Type checking            │   │
│  │  - Range validation         │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │  Error Handling             │   │
│  │  - Try-catch blocks         │   │
│  │  - Safe error messages      │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │  Access Control             │   │
│  │  - Health endpoints         │   │
│  │  - Rate limiting (future)   │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

## Scalability Design

### Horizontal Scaling
```
Load Balancer
     │
     ├─── Instance 1 (Flask + Gunicorn)
     │
     ├─── Instance 2 (Flask + Gunicorn)
     │
     └─── Instance 3 (Flask + Gunicorn)
```

### Vertical Scaling
- Increase Gunicorn workers
- Optimize model loading
- Use caching layers

## File Structure Map

```
housing1/
├── .github/workflows/       # CI/CD
├── configs/                 # Configuration
├── data/                    # Data storage
├── models/                  # Model artifacts
├── pipelines/               # ML pipelines
├── src/                     # Source code
│   ├── config.py           # Configuration
│   ├── data.py             # Data handling
│   ├── model.py            # Model ops
│   ├── tracking.py         # Experiment tracking
│   ├── validation.py       # Validation
│   └── monitoring.py       # Monitoring
├── tests/                   # Tests
├── api.py                   # API server
├── Makefile                # Commands
├── docker-compose.yml      # Docker orchestration
└── requirements.txt        # Dependencies
```

## Communication Protocols

### Internal (Module to Module)
- Direct function calls
- Shared configuration
- Common interfaces

### External (API)
- REST over HTTP
- JSON payload
- Standard status codes

### Asynchronous (Future)
- Message queues (RabbitMQ/Kafka)
- Task queues (Celery)
- Event-driven architecture

---

This architecture supports:
- ✅ **Modularity**: Clear separation of concerns
- ✅ **Scalability**: Easy to scale horizontally
- ✅ **Maintainability**: Clean, documented code
- ✅ **Testability**: Comprehensive test suite
- ✅ **Monitoring**: Built-in observability
- ✅ **Flexibility**: Easy to extend and modify
