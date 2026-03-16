#!/bin/bash
# Deployment script for House Price Prediction App

set -e  # Exit on any error

echo "🚀 Deploying House Price Prediction Application..."

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.6+."
    exit 1
fi

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip."
    exit 1
fi

echo "✅ Python and pip are available"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🔨 Creating virtual environment..."
    python -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate.bat 2>/dev/null || true

# Upgrade pip
echo "⬆️ Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Dependencies installed"

# Check if data directory exists
if [ ! -f "Data/house_price.csv" ]; then
    echo "❌ Data file Data/house_price.csv not found!"
    echo "Please place your house price data file in the Data/ directory."
    exit 1
fi

echo "✅ Data file found"

# Run the application
echo "🎮 Starting the House Price Prediction application..."
echo "🌐 Access the application at: http://localhost:5000"
echo "🔄 Press Ctrl+C to stop the application"

# Start the Flask app
python app.py
