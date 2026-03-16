import os
import sys

# Add the housing1 directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'House_Price_Prediction-main', 'housing1'))

# Change to the housing1 directory for relative paths
os.chdir(os.path.join(os.path.dirname(__file__), 'House_Price_Prediction-main', 'housing1'))

# Import the actual app
from app import app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
