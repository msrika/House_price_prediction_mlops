@echo off
REM Deployment batch script for House Price Prediction App
REM For Windows systems

echo 🚀 Deploying House Price Prediction Application...

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.6+.
    pause
    exit /b 1
)

echo ✅ Python is available

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 🔨 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

echo ✅ Dependencies installed

REM Check if data directory exists
if not exist "Data\house_price.csv" (
    echo ❌ Data file Data/house_price.csv not found!
    echo Please place your house price data file in the Data/ directory.
    pause
    exit /b 1
)

echo ✅ Data file found

REM Run the application
echo 🎮 Starting the House Price Prediction application...
echo 🌐 Access the application at: http://localhost:5000
echo 🔄 Press Ctrl+C to stop the application

REM Start the Flask app
python app.py

pause