# MLOps House Price Prediction - Makefile

.PHONY: help install train test lint clean docker-build docker-run api deploy

# Default target
help:
	@echo "MLOps House Price Prediction - Available Commands:"
	@echo ""
	@echo "  make install          - Install all dependencies"
	@echo "  make train            - Run training pipeline"
	@echo "  make test             - Run tests"
	@echo "  make test-cov         - Run tests with coverage"
	@echo "  make lint             - Run code linters"
	@echo "  make type-check       - Run type checking"
	@echo "  make validate-data    - Validate data quality"
	@echo "  make api              - Start prediction API"
	@echo "  make docker-build     - Build Docker image"
	@echo "  make docker-run       - Run Docker container"
	@echo "  make clean            - Clean up artifacts"
	@echo "  make setup            - Initial project setup"
	@echo ""

# Installation
install:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	@echo "✓ Installation complete"

# Development installation
install-dev:
	pip install -e .
	pip install pytest pytest-cov flake8 mypy black isort
	@echo "✓ Development installation complete"

# Training Pipeline
train:
	python pipelines/train.py --target Price

train-rf:
	python pipelines/train.py --target Price --model-type random_forest

# Testing
test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing

test-fast:
	pytest tests/ -v -k "not slow"

# Code Quality
lint:
	flake8 src/ pipelines/ api.py --max-line-length=120 --show-source
	@echo "✓ Linting complete"

type-check:
	mypy src/ --ignore-missing-imports
	@echo "✓ Type checking complete"

format:
	black src/ pipelines/ tests/ api.py
	isort src/ pipelines/ tests/ api.py
	@echo "✓ Formatting complete"

# Data Validation
validate-data:
	python -c "from src.data import DataLoader; from src.validation import DataValidator; \
	loader = DataLoader(); df = loader.load_data(); \
	validator = DataValidator(); \
	report = validator.validate_data_quality(df); \
	validator.print_validation_report()"

# API
api:
	python api.py

api-prod:
	gunicorn -w 4 -b 0.0.0.0:5000 api:app

# Docker
docker-build:
	docker build -t house-price-prediction:latest .

docker-run:
	docker run -p 5000:5000 house-price-prediction:latest

docker-stop:
	docker stop $$(docker ps -q --filter ancestor=house-price-prediction) || true

# Model Registry
register-model:
	python -c "from src.tracking import ModelRegistry; \
registry = ModelRegistry(); \
print('Registered models:', registry.list_models())"

# Monitoring
monitor:
	python -c "from src.monitoring import MonitoringLogger; \
logger = MonitoringLogger(); \
print('Monitoring logs available in logs/ directory')"

# Experiment Tracking
experiments:
	python -c "from src.tracking import ExperimentTracker; \
tracker = ExperimentTracker(); \
runs = tracker.get_all_runs(); \
print(f'Total runs: {len(runs)}'); \
for run in runs: print(f\"  - {run['run_name']}: {run['status']}\")"

best-experiment:
	python -c "from src.tracking import ExperimentTracker; \
tracker = ExperimentTracker(); \
best = tracker.get_best_run(metric='r2'); \
print('Best experiment:', best)"

# CI/CD
ci: lint test type-check
	@echo "✓ All CI checks passed"

cd: docker-build
	@echo "✓ CD pipeline ready"

# Setup
setup:
	mkdir -p data/raw data/processed models artifacts logs experiments
	cp configs/config.yaml configs/config.yaml.backup 2>/dev/null || true
	@echo "✓ Project setup complete"

# Clean
clean:
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf logs/*
	rm -rf models/*.pkl
	rm -rf artifacts/*
	rm -rf experiments/*/run_*
	@echo "✓ Cleanup complete"

# Production deployment
deploy:
	@echo "🚀 Deploying to production..."
	# Add your deployment commands here
	# Example: kubectl apply -f k8s/
	# Example: docker-compose -f docker-compose.prod.yml up -d
	@echo "✓ Deployment complete"

# Health check
health:
	curl -f http://localhost:5000/health || echo "API not running"

# Version
version:
	@echo "MLOps House Price Prediction v1.0.0"
