# 🏠 MLOps House Price Prediction

A production-ready MLOps project for house price prediction with complete CI/CD pipeline, monitoring, and model management.

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![MLOps](https://img.shields.io/badge/MLOps-Production%20Ready-orange)

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [MLOps Components](#mlops-components)
- [API Endpoints](#api-endpoints)
- [Monitoring](#monitoring)
- [Testing](#testing)
- [CI/CD Pipeline](#cicd-pipeline)
- [Docker](#docker)
- [Railway Deployment](#railway-deployment)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### 🎯 Core Features
- **Modular Architecture**: Clean separation of concerns with reusable components
- **Automated Training Pipeline**: End-to-end ML workflow automation
- **Experiment Tracking**: Track and compare model experiments
- **Model Registry**: Version control for your models
- **Data Validation**: Automated data quality checks
- **Drift Detection**: Monitor data drift in production
- **Performance Monitoring**: Real-time model performance tracking
- **RESTful API**: Production-ready prediction API
- **Data Visualizations**: Comprehensive data analysis and visualization
- **Modern UI**: Beautiful interface with background effects and animations
- **Comprehensive Testing**: Unit, integration, and end-to-end tests
- **CI/CD Pipeline**: Automated testing and deployment
- **Railway Deployment Ready**: Easy deployment to Railway cloud platform

### 🛠️ Technical Features
- Configuration management with YAML
- Type hints for better code quality
- Comprehensive logging and monitoring
- Docker support for containerization
- GitHub Actions for CI/CD
- Makefile for common operations
- Code linting and formatting

## 📁 Project Structure

```
housing1/
├── .github/workflows/       # CI/CD pipeline configurations
│   └── mlops_pipeline.yml
├── configs/                 # Configuration files
│   └── config.yaml
├── data/                    # Data directories
│   ├── raw/                # Raw data
│   └── processed/          # Processed data
├── models/                  # Trained models
│   └── registry/           # Model registry
├── pipelines/              # ML pipelines
│   └── train.py           # Training pipeline
├── src/                    # Source code
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── data.py            # Data loading & preprocessing
│   ├── model.py           # Model training & evaluation
│   ├── tracking.py        # Experiment tracking & registry
│   ├── validation.py      # Data validation & drift detection
│   └── monitoring.py      # Performance monitoring
├── static/                 # Static files (CSS, JS, images)
│   ├── css/               # Style sheets
│   │   └── style.css      # Main styling with background effects
│   └── images/            # Image assets
├── templates/              # HTML templates
│   └── index.html         # Main UI with visualizations
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── conftest.py
│   └── test_components.py
├── api.py                  # Flask API
├── app.py                  # Main Flask application (Railway ready)
├── visualization.py        # Data visualization module
├── requirements.txt        # Python dependencies
├── requirements-dev.txt    # Development dependencies
├── Makefile               # Common commands
├── Dockerfile             # Docker configuration (Railway ready)
├── Procfile               # Process definition for Railway
├── railway.json           # Railway configuration
├── deploy_to_railway.sh   # Railway deployment script (Unix)
├── deploy_to_railway.bat  # Railway deployment script (Windows)
└── README.md              # This file
```

## 🚀 Quick Start

```bash
# Clone the repository
git clone <your-repo-url>
cd housing1

# Install dependencies
make install

# Train a model
make train

# Run the API
make api

# Visit http://localhost:5000
```

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Git

### Step-by-step Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd housing1
```

2. **Create virtual environment (optional but recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
make install
# Or manually:
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

4. **Setup project structure**
```bash
make setup
```

5. **Verify installation**
```bash
make test
```

## 💻 Usage

### Training a Model

```bash
# Using Makefile
make train

# Or directly
python pipelines/train.py --target Price
```

### Running the API

```bash
# Development mode
make api

# Production mode
make api-prod

# Or directly
python app.py
```

### Making Predictions

```bash
# Via CLI
curl -X POST http://localhost:5000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Area": 2000,
    "Bedrooms": 3,
    "Bathrooms": 2,
    "Stories": 2,
    "Parking": 1,
    "Age": 5,
    "Location": 3
  }'
```

## 🚂 Railway Deployment

Your application is now ready for deployment to Railway! Follow these steps to get your own public URL like `https://your-app-name.up.railway.app/`.

### Prerequisites
- Railway account at [railway.app](https://railway.app)
- Git installed on your system
- All required files in your project directory

### Deployment Methods

#### Method 1: Using Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project (in your app directory)
railway init

# Link to your Railway project
railway link

# Deploy
railway up
```

#### Method 2: Using Railway Dashboard
1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Choose "Deploy from GitHub" or upload your project files
4. Railway will automatically detect and deploy your application

#### Method 3: Using Git
```bash
# Initialize git in your project directory
git init
git add .
git commit -m "Initial commit for Railway deployment"

# Connect to Railway git remote (get from Railway dashboard)
git remote add railway YOUR_RAILWAY_GIT_URL
git push railway main
```

### Required Files for Railway
Your project includes all necessary files for Railway deployment:
- `Dockerfile` - Container configuration
- `Procfile` - Process definition
- `railway.json` - Railway-specific configuration
- `requirements.txt` - Python dependencies
- `app.py` - Main application (configured for Railway)

### Environment Variables
Railway automatically sets the `PORT` environment variable. The application is configured to use this automatically.

### Accessing Your Deployed App
After successful deployment, you'll receive a URL in the format:
```
https://your-project-name.up.railway.app/
```

### Troubleshooting Railway Deployment
- Check logs: `railway logs`
- Verify all files are included in deployment
- Ensure Data/house_price.csv exists
- Confirm requirements.txt has all necessary dependencies

## 🔧 MLOps Components

### 1. Configuration Management

Centralized configuration in `configs/config.yaml`:

```yaml
project:
  name: "House Price Prediction"
  version: "1.0.0"

data:
  raw_path: "data/raw/house_price.csv"
  test_size: 0.2

model:
  type: "linear_regression"
  save_path: "models/"
```

### 2. Data Pipeline

```python
from src.data import DataLoader, DataPreprocessor

# Load data
loader = DataLoader()
df = loader.load_data()

# Preprocess
preprocessor = DataPreprocessor()
X, y = preprocessor.prepare_features(df, 'Price')
X_train, X_test, y_train, y_test = preprocessor.split_data(X, y)
```

### 3. Model Training

```python
from src.model import ModelTrainer, ModelEvaluator

# Train
trainer = ModelTrainer(model_type='linear_regression')
model = trainer.train(X_train, y_train)

# Evaluate
evaluator = ModelEvaluator()
metrics = evaluator.evaluate(model, X_test, y_test)
```

### 4. Experiment Tracking

```python
from src.tracking import ExperimentTracker

tracker = ExperimentTracker()

# Start run
run_id = tracker.start_run('experiment_1')

# Log parameters
tracker.log_parameters({'learning_rate': 0.01})

# Log metrics
tracker.log_metrics({'accuracy': 0.95})

# End run
tracker.end_run(status='completed')
```

### 5. Model Registry

```python
from src.tracking import ModelRegistry

registry = ModelRegistry()

# Register model
registry.register_model(
    model_path='models/model.pkl',
    version='1.0.0',
    metrics={'r2': 0.85, 'mae': 1000},
    description='Production model'
)

# Get latest model
latest = registry.get_latest_model()
```

### 6. Data Validation

```python
from src.validation import DataValidator, DriftDetector

# Validate data quality
validator = DataValidator()
report = validator.validate_data_quality(df)
validator.print_validation_report()

# Detect drift
detector = DriftDetector()
detector.fit(reference_data)
drift_results = detector.detect_drift(current_data)
```

### 7. Monitoring

```python
from src.monitoring import MonitoringLogger

monitor = MonitoringLogger()

# Log predictions
monitor.log_prediction(
    input_data={'Area': 2000},
    prediction=250000
);

# Log performance
monitor.log_performance({'r2': 0.85, 'mae': 1000});
```

## 🌐 API Endpoints

### Home Page
```
GET /
```

### Predict (Form)
```
POST /predict
Content-Type: application/x-www-form-urlencoded
```

### Predict (REST API)
```
POST /api/v1/predict
Content-Type: application/json

{
  "Area": 2000,
  "Bedrooms": 3,
  "Bathrooms": 2,
  "Stories": 2,
  "Parking": 1,
  "Age": 5,
  "Location": 3
}
```

### Health Check
```
GET /health
```

### Metrics
```
GET /metrics
```

### Visualizations
```
GET /visualize
GET /dashboard
```

## 📊 Monitoring

### Logs Location
- Application logs: `logs/app.log`
- Monitoring logs: `logs/monitoring.log`
- Predictions: `logs/predictions_*.json`
- Performance: `logs/performance_*.json`

### Metrics Tracked
- Prediction volume
- Model performance (MAE, MSE, RMSE, R²)
- Data drift scores
- Response times
- Error rates

## 🧪 Testing

```bash
# Run all tests
make test

# Run tests with coverage
make test-cov

# Run specific test file
pytest tests/test_components.py -v

# Run fast tests only
make test-fast
```

## 🔄 CI/CD Pipeline

The GitHub Actions pipeline includes:

1. **Test Stage**
   - Linting (flake8)
   - Unit tests (pytest)
   - Type checking (mypy)
   - Code coverage

2. **Build Stage**
   - Docker image build
   - Artifact creation

3. **Validation Stage**
   - Model training validation
   - Performance threshold checks

4. **Deploy Stage**
   - Deploy to staging
   - Integration tests
   - Deploy to production

## 🐳 Docker

### Build Image
```bash
make docker-build
# Or
docker build -t house-price-prediction:latest .
```

### Run Container
```bash
make docker-run
# Or
docker run -p 5000:5000 house-price-prediction:latest
```

### Stop Container
```bash
make docker-stop
```

## ⚙️ Configuration

Edit `configs/config.yaml` to customize:

- Data paths and parameters
- Model hyperparameters
- Training settings
- Monitoring thresholds
- API configuration
- Logging levels

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Write tests for new features
- Follow PEP 8 style guidelines
- Add type hints to functions
- Update documentation as needed
- Use meaningful commit messages

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- MLOps Team

## 🙏 Acknowledgments

- Scikit-learn team for excellent ML library
- Flask team for the web framework
- All open-source contributors

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Contact: team@example.com

---

**Made with ❤️ using MLOps best practices**

**Ready for Railway deployment! 🚂 Get your own `.up.railway.app` URL!**