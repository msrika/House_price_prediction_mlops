#!/bin/bash
# Railway Deployment Script for House Price Prediction App

echo "🚀 Preparing House Price Prediction App for Railway Deployment..."

# Check if in the correct directory
if [ ! -f "app.py" ] || [ ! -f "requirements.txt" ] || [ ! -f "Procfile" ]; then
    echo "❌ Required files not found!"
    echo "Make sure you're in the housing1 directory with app.py, requirements.txt, and Procfile"
    exit 1
fi

echo "✅ Required files found"

# Check for data file
if [ ! -f "Data/house_price.csv" ]; then
    echo "❌ Data file Data/house_price.csv not found!"
    echo "Please ensure your data file is in the Data/ directory"
    exit 1
fi

echo "✅ Data file found"

# Check for templates
if [ ! -d "templates" ] || [ ! -f "templates/index.html" ]; then
    echo "❌ Templates directory or index.html not found!"
    exit 1
fi

echo "✅ Templates found"

# Check for static files
if [ ! -d "static" ]; then
    echo "⚠️ Static directory not found, creating..."
    mkdir -p static/css static/images
fi

echo "✅ Static files structure OK"

echo ""
echo "📋 Files ready for Railway deployment:"
echo "- app.py (with Railway-compatible configuration)"
echo "- requirements.txt (dependencies)"
echo "- Procfile (process definition)"
echo "- Dockerfile (container configuration)"
echo "- Data/house_price.csv (training data)"
echo "- templates/ (HTML templates)"
echo "- static/ (CSS and images)"
echo "- railway.json (Railway configuration)"

echo ""
echo "🚀 To deploy to Railway:"
echo ""
echo "Method 1 - Railway CLI:"
echo "  1. Install: npm install -g @railway/cli"
echo "  2. Login: railway login"
echo "  3. Deploy: railway up"
echo ""
echo "Method 2 - Railway Dashboard:"
echo "  1. Go to https://railway.app"
echo "  2. Create new project"
echo "  3. Connect to your GitHub repo or upload files"
echo ""
echo "Method 3 - Git:"
echo "  1. git init"
echo "  2. git add ."
echo "  3. git commit -m 'Deploy to Railway'"
echo "  4. Connect to Railway git remote and push"
echo ""
echo "🔗 After deployment, your app will be available at:"
echo "   https://your-project-name.up.railway.app/"
echo ""

echo "✅ Deployment preparation complete!"
echo "📖 For detailed instructions, see RAILWAY_DEPLOYMENT.md"