@echo off
REM Railway Deployment Script for House Price Prediction App (Windows)

echo 🚀 Preparing House Price Prediction App for Railway Deployment...

REM Check if in the correct directory
if not exist "app.py" (
    echo ❌ app.py not found!
    echo Make sure you're in the housing1 directory
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo ❌ requirements.txt not found!
    pause
    exit /b 1
)

if not exist "Procfile" (
    echo ❌ Procfile not found!
    pause
    exit /b 1
)

echo ✅ Required files found

REM Check for data file
if not exist "Data\house_price.csv" (
    echo ❌ Data file Data/house_price.csv not found!
    echo Please ensure your data file is in the Data/ directory
    pause
    exit /b 1
)

echo ✅ Data file found

REM Check for templates
if not exist "templates" (
    echo ❌ Templates directory not found!
    pause
    exit /b 1
)

if not exist "templates\index.html" (
    echo ❌ templates/index.html not found!
    pause
    exit /b 1
)

echo ✅ Templates found

REM Check for static files
if not exist "static" (
    echo ⚠️ Static directory not found, creating...
    mkdir static
    mkdir static\css
    mkdir static\images
)

echo ✅ Static files structure OK

echo.
echo 📋 Files ready for Railway deployment:
echo   - app.py (with Railway-compatible configuration)
echo   - requirements.txt (dependencies)
echo   - Procfile (process definition)
echo   - Dockerfile (container configuration)
echo   - Data/house_price.csv (training data)
echo   - templates/ (HTML templates)
echo   - static/ (CSS and images)
echo   - railway.json (Railway configuration)

echo.
echo 🚀 To deploy to Railway:
echo.
echo Method 1 - Railway CLI:
echo   1. Install: npm install -g @railway/cli
echo   2. Login: railway login
echo   3. Deploy: railway up
echo.
echo Method 2 - Railway Dashboard:
echo   1. Go to https://railway.app
echo   2. Create new project
echo   3. Connect to your GitHub repo or upload files
echo.
echo Method 3 - Git:
echo   1. git init
echo   2. git add .
echo   3. git commit -m "Deploy to Railway"
echo   4. Connect to Railway git remote and push
echo.
echo 🔗 After deployment, your app will be available at:
echo    https://your-project-name.up.railway.app/
echo.

echo ✅ Deployment preparation complete!
echo 📖 For detailed instructions, see RAILWAY_DEPLOYMENT.md

pause