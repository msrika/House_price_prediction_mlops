# MLOps House Price Prediction - Setup Guide

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10 or higher**
- **pip** (Python package manager)
- **Git**
- **Docker** (optional, for containerization)

## Installation Steps

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd housing1
```

### 2. Create Virtual Environment

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/Mac
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt
```

### 4. Project Setup

```bash
# Create necessary directories
make setup

# Or manually create directories
mkdir -p data/raw data/processed models artifacts logs experiments
```

### 5. Verify Installation

```bash
# Run tests to verify everything works
make test
```

## Configuration

1. Open `configs/config.yaml`
2. Update paths and parameters as needed
3. Set appropriate logging levels

## Data Preparation

Place your raw data file in `data/raw/house_price.csv`

The CSV should contain:
- Feature columns (Area, Bedrooms, Bathrooms, Stories, Parking, Age, Location)
- Target column (Price)

## Quick Start

```bash
# Train a model
make train

# Start the API server
make api

# Visit http://localhost:5000 in your browser
```

## Troubleshooting

### Common Issues

**Import Errors**
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Port Already in Use**
```bash
# Change port in configs/config.yaml
api:
  port: 5001
```

**Model Not Found**
```bash
# Train a new model first
make train
```

## Next Steps

1. ✅ Complete installation
2. ✅ Train initial model
3. ✅ Test API endpoints
4. ✅ Review monitoring setup
5. ✅ Configure CI/CD pipeline

For detailed usage, see [README.md](README.md)
