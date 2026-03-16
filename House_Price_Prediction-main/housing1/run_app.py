import subprocess
import sys
import os
from pathlib import Path

def check_and_install_dependencies():
    """Check if required packages are installed, install if not."""
    required_packages = [
        "flask",
        "pandas", 
        "numpy",
        "scikit-learn"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Installing missing packages: {missing_packages}")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
        print("Dependencies installed successfully!")

def main():
    """Main function to run the house price prediction app."""
    print("🏠 House Price Prediction Application")
    print("="*50)
    
    # Check and install dependencies
    print("Checking dependencies...")
    check_and_install_dependencies()
    
    # Verify data file exists
    data_path = Path("Data/house_price.csv")
    if not data_path.exists():
        print(f"❌ Error: Data file {data_path} not found!")
        print("Please ensure your data file is in the Data/ directory.")
        input("Press Enter to exit...")
        return
    
    print(f"✅ Data file found: {data_path}")
    print("✅ All dependencies are available")
    
    print("\n🚀 Starting the application...")
    print("🌐 Access the application at: http://localhost:5000")
    print("🔄 Press Ctrl+C to stop the application\n")
    
    try:
        # Run the Flask app
        import app
        app.app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user.")
    except Exception as e:
        print(f"❌ Error running application: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()