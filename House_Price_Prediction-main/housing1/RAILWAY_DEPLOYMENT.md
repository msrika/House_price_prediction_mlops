# 🚂 Deploying House Price Prediction to Railway

This guide will walk you through deploying your House Price Prediction application to Railway to get a public URL like `https://your-app-name.up.railway.app/`.

## 📋 Prerequisites

- **Railway Account**: Sign up at [railway.app](https://railway.app)
- **Git**: Installed on your system
- **Data File**: Make sure your `Data/house_price.csv` is in the correct location
- **GitHub Account**: (Optional but recommended) to connect with Railway

## 🚀 Deployment Steps

### Method 1: Using Railway CLI (Recommended)

1. **Install Railway CLI**
   ```bash
   # For Windows (using npm)
   npm install -g @railway/cli
   
   # Or using curl
   curl -fsSL https://railway.app/install.sh | sh
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize Railway project in your app directory**
   ```bash
   cd c:\Users\Srika\Downloads\House_Price_Prediction-main\House_Price_Prediction-main\housing1
   railway init
   ```

4. **Link your project**
   ```bash
   railway link
   ```

5. **Deploy**
   ```bash
   railway up
   ```

### Method 2: Using Railway Dashboard

1. **Go to [railway.app](https://railway.app)**
2. **Click "New Project"**
3. **Choose "Deploy from GitHub" or "Deploy from Template"**
4. **If using GitHub:**
   - Connect your GitHub account
   - Select your repository containing the House Price Prediction app
   - Railway will automatically detect and deploy your app

5. **If deploying manually:**
   - Create a new project
   - Upload your project files
   - Make sure all files are included:
     - `app.py`
     - `requirements.txt`
     - `Procfile`
     - `Dockerfile`
     - `templates/` folder
     - `static/` folder
     - `Data/house_price.csv`
     - `visualization.py`

### Method 3: Using Git

1. **Initialize git in your project directory**
   ```bash
   cd c:\Users\Srika\Downloads\House_Price_Prediction-main\House_Price_Prediction-main\housing1
   git init
   git add .
   git commit -m "Initial commit for Railway deployment"
   ```

2. **Connect to Railway via Git**
   ```bash
   # Get the Railway git remote URL from your project dashboard
   git remote add railway YOUR_RAILWAY_GIT_URL
   git push railway main
   ```

## ⚙️ Railway Configuration

Your project is already configured for Railway with:

### Files Included:
- **`Dockerfile`**: Defines the container environment
- **`Procfile`**: Specifies how to run the application
- **`railway.json`**: Railway-specific configuration
- **`requirements.txt`**: Python dependencies
- **Environment variables**: PORT is automatically handled

### Environment Variables:
Railway automatically sets:
- `PORT`: The port number to bind to (handled in app.py)

## 🏗️ Project Structure for Railway

Make sure your project has these files in the root directory:

```
housing1/
├── app.py                 # Main Flask application
├── visualization.py       # Visualization module
├── requirements.txt       # Python dependencies
├── Procfile               # Process type definition
├── Dockerfile             # Container configuration
├── railway.json           # Railway configuration
├── templates/             # HTML templates
│   └── index.html
├── static/                # Static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css
│   └── images/
├── Data/                  # Data directory
│   └── house_price.csv
└── README.md              # Documentation
```

## 🔧 Troubleshooting

### Common Issues:

**1. Build fails due to dependencies:**
- Check that all dependencies in `requirements.txt` are compatible
- Some packages might need build tools (included in Dockerfile)

**2. Application crashes after deployment:**
- Check Railway logs: `railway logs`
- Verify the PORT environment variable is being used
- Ensure all required files are included

**3. Static files not loading:**
- Make sure the `static/` folder is in the correct location
- Flask is configured to serve static files

**4. Data file not found:**
- Ensure `Data/house_price.csv` is in the correct location
- The path should be relative to the app.py file

## 🌐 Accessing Your Deployed App

Once deployed successfully:
1. Railway will provide a URL like `https://your-app-name.up.railway.app/`
2. You can also set up a custom domain if desired
3. The application will be publicly accessible

## 🔄 Continuous Deployment

To enable automatic deployments:
1. Connect your GitHub repository to Railway
2. Every push to the main branch will trigger a new deployment
3. You can configure deployment triggers in the Railway dashboard

## 🛠️ Managing Your Deployment

### View logs:
```bash
railway logs
```

### Open your app:
```bash
railway open
```

### View environment variables:
```bash
railway vars
```

## 📊 Features Available

Your deployed application will include:
- ✅ House price prediction form
- ✅ Data visualizations
- ✅ Interactive dashboard
- ✅ Modern UI with background effects
- ✅ Responsive design
- ✅ Professional styling

## 🎯 Expected URL Format

After successful deployment, you'll get a URL in this format:
```
https://your-project-name.up.railway.app/
```

Replace `your-project-name` with whatever you name your Railway project.

## 📞 Support

For Railway-specific issues:
- Check Railway documentation: [docs.railway.app](https://docs.railway.app)
- Join Railway Discord community
- Check Railway status: [status.railway.app](https://status.railway.app)

---

**🎉 Your House Price Prediction app is now ready for Railway deployment! Follow the steps above to get your own public URL ending in `.up.railway.app`**