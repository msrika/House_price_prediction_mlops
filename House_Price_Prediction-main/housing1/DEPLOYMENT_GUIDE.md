# 🚀 Deployment Guide for House Price Prediction App

## 📋 Deployment Options

Choose one of the following deployment methods:

## Option 1: Local Development Deployment (Recommended for testing)

### Prerequisites
- Python 3.6 or higher
- pip package manager

### Steps

1. **Open Command Prompt or Terminal**
   ```cmd
   cd c:\Users\Srika\Downloads\House_Price_Prediction-main\House_Price_Prediction-main\housing1
   ```

2. **Run the deployment script** (Windows):
   ```cmd
   deploy.bat
   ```

   Or on Linux/Mac:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

3. **Access the application**
   - Open your browser
   - Go to: `http://localhost:5000`
   - The application should be running

## Option 2: Manual Deployment

### Steps

1. **Navigate to the project directory**
   ```cmd
   cd c:\Users\Srika\Downloads\House_Price_Prediction-main\House_Price_Prediction-main\housing1
   ```

2. **Create a virtual environment**
   ```cmd
   python -m venv venv
   ```

3. **Activate the virtual environment**
   ```cmd
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```cmd
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```cmd
   python app.py
   ```

6. **Access the application**
   - Open your browser
   - Go to: `http://localhost:5000`

## Option 3: Production Deployment with Gunicorn

### Prerequisites
- Python 3.6+
- Gunicorn (already included in requirements.txt)

### Steps

1. **Install dependencies**
   ```cmd
   pip install -r requirements.txt
   ```

2. **Run with Gunicorn** (requires app.py to be properly configured)
   ```cmd
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

## Option 4: Docker Deployment

### Prerequisites
- Docker installed on your system

### Steps

1. **Build the Docker image**
   ```cmd
   docker build -t house-price-prediction .
   ```

2. **Run the Docker container**
   ```cmd
   docker run -p 5000:5000 house-price-prediction
   ```

3. **Access the application**
   - Open your browser
   - Go to: `http://localhost:5000`

## 📁 Directory Structure Expected

Make sure your directory structure looks like this:

```
housing1/
├── app.py                 # Main Flask application
├── Data/
│   └── house_price.csv    # Training data
├── templates/
│   └── index.html         # Frontend template
├── requirements.txt       # Dependencies
├── deploy.bat             # Windows deployment script
├── deploy.sh              # Unix deployment script
└── ...
```

## 🛠️ Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'flask'`
**Solution**: Run `pip install -r requirements.txt`

**Issue**: `FileNotFoundError: [Errno 2] No such file or directory: 'Data/house_price.csv'`
**Solution**: Ensure the data file exists in the Data/ directory

**Issue**: `Permission denied` on port 5000
**Solution**: Use a different port by modifying app.py or kill the process using port 5000

**Issue**: Port already in use
**Solution**: 
- On Windows: `netstat -ano | findstr :5000` to find PID, then `taskkill /PID <PID> /F`
- On Linux/Mac: `lsof -i :5000` to find PID, then `kill -9 <PID>`

### Check Application Status

1. **Verify the application is running**
   ```cmd
   curl http://localhost:5000/
   ```
   Or visit `http://localhost:5000/` in your browser

2. **Check if the model loaded successfully**
   Look for messages in the console like:
   ```
   Loading data...
   Model trained successfully!
   * Running on http://127.0.0.1:5000
   ```

## 🌐 Accessing the Application

Once deployed successfully:

1. **Open your web browser**
2. **Go to**: `http://localhost:5000`
3. **You should see**: "House Price Prediction" form
4. **Fill in the house details**:
   - Area (sqft)
   - Number of Bedrooms
   - Number of Bathrooms
   - Number of Stories
   - Parking spaces
   - Age of the house
   - Location (City, Suburban, Rural)
5. **Click "Predict Price"**
6. **See the predicted price** displayed in green

## 🛑 Stopping the Application

To stop the running application:
- Press `Ctrl+C` in the terminal/command prompt where it's running

## 📊 Sample Data Format

The application expects a CSV file with the following columns:
```
Area,Bedrooms,Bathrooms,Stories,Parking,Age,Location,Price
1200,2,1,1,1,10,1,3500000
1500,3,2,1,1,5,1,4800000
...
```

## 🚀 Production Notes

For production deployment:
- Use a production WSGI server like Gunicorn
- Set `debug=False` in app.py
- Use environment variables for configuration
- Implement proper logging
- Add authentication if needed
- Use a reverse proxy like Nginx

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are met
3. Ensure the data file exists and is properly formatted
4. Check that all dependencies are installed

---

**🎉 Your House Price Prediction application is ready to deploy!**