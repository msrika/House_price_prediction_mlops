# 🚀 Quick Start Guide

## 1-Minute Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Setup project structure
python setup.py

# Train a model
python pipelines/train.py --target Price

# Start API server
python api.py

# Visit http://localhost:5000
```

## Using Make (Recommended)

```bash
# Install everything
make install

# Setup directories
make setup

# Train model
make train

# Start API
make api

# Open browser to http://localhost:5000
```

## Using Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build and run manually
docker build -t house-price-prediction .
docker run -p 5000:5000 house-price-prediction
```

## Test the API

```bash
# Health check
curl http://localhost:5000/health

# Make prediction
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

## Next Steps

- ✅ Read [SETUP.md](SETUP.md) for detailed installation
- ✅ Read [README.md](README.md) for full documentation
- ✅ Configure settings in `configs/config.yaml`
- ✅ Add your data to `data/raw/house_price.csv`

## Common Commands

```bash
make test          # Run tests
make lint          # Check code style
make train         # Train model
make api           # Start API server
make clean         # Clean artifacts
make docker-build  # Build Docker image
make docker-run    # Run Docker container
```

## Troubleshooting

**Port already in use?**
```bash
# Change port in configs/config.yaml
api:
  port: 5001
```

**Model not found?**
```bash
# Train a new model
make train
```

**Tests failing?**
```bash
# Reinstall dependencies
make install-dev
```

---

For complete documentation, see [README.md](README.md)
