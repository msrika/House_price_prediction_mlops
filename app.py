import os
import sys

# Get the absolute path to the housing1 directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
housing1_path = os.path.join(BASE_DIR, 'House_Price_Prediction-main', 'housing1')

# Add to Python path for imports
sys.path.insert(0, housing1_path)

# Change working directory for relative file paths
os.chdir(housing1_path)

# Import the Flask app from the nested directory
from app import app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
